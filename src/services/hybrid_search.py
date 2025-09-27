from typing import List, Dict
from ..clients.opensearch import get_client
from ..settings import settings
from .embed import embed_query

INDEX = settings.os_index
BM25_FIELDS = ["title^2", "abstract^1.5", "text^1"]
VECTOR_DIMS = 384 if settings.embedding_provider.lower() == "sbert" else 8

def ensure_index():
    os = get_client()
    if not os.indices.exists(index=INDEX):
        os.indices.create(
            index=INDEX,
            body={
                "settings": {"index": {"similarity": {"default": {"type": "BM25"}}}},
                "mappings": {
                    "properties": {
                        "doc_id": {"type": "keyword"},
                        "paper_id": {"type": "integer"},
                        "chunk_id": {"type": "integer"},
                        "title": {"type": "text"},
                        "abstract": {"type": "text"},
                        "text": {"type": "text"},
                        "vector": {"type": "dense_vector", "dims": VECTOR_DIMS, "index": False},
                    }
                },
            },
        )

def index_chunk(doc: Dict):
    get_client().index(index=INDEX, body=doc, id=doc["doc_id"], refresh=True)

def _bm25_search(query: str, size: int = 20) -> List[Dict]:
    res = get_client().search(
        index=INDEX,
        body={"size": size, "query": {"multi_match": {"query": query, "fields": BM25_FIELDS}}},
    )
    hits = res.get("hits", {}).get("hits", [])
    out = []
    for h in hits:
        src = h.get("_source", {})
        out.append({
            "doc_id": src.get("doc_id"),
            "paper_id": src.get("paper_id"),
            "chunk_id": src.get("chunk_id"),
            "title": src.get("title"),
            "abstract": src.get("abstract"),
            "text": src.get("text",""),
            "bm25": float(h.get("_score", 0.0)),
        })
    return out

def _vector_search(query: str, size: int = 20) -> List[Dict]:
    qvec = embed_query(query)
    res = get_client().search(
        index=INDEX,
        body={
            "size": size,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                        "params": {"query_vector": qvec},
                    },
                }
            },
        },
    )
    hits = res.get("hits", {}).get("hits", [])
    out = []
    for h in hits:
        src = h.get("_source", {})
        out.append({
            "doc_id": src.get("doc_id"),
            "paper_id": src.get("paper_id"),
            "chunk_id": src.get("chunk_id"),
            "title": src.get("title"),
            "abstract": src.get("abstract"),
            "text": src.get("text",""),
            "vec": float(h.get("_score", 0.0)),  # [0..2] due to +1.0
        })
    return out

def hybrid_search(query: str, bm25_k: int = 20, vec_k: int = 20, alpha: float | None = None, top_k: int = 10) -> List[Dict]:
    alpha = settings.hybrid_alpha if alpha is None else alpha
    bm25_results = _bm25_search(query, size=bm25_k)
    vec_results = _vector_search(query, size=vec_k)

    # merge by doc_id
    by_id: Dict[str, Dict] = {}
    for d in bm25_results:
        by_id[d["doc_id"]] = {**d, "vec": 0.0}
    for d in vec_results:
        if d["doc_id"] in by_id:
            by_id[d["doc_id"]]["vec"] = d["vec"]
        else:
            by_id[d["doc_id"]] = {**d, "bm25": 0.0}

    # normalize bm25 (min-max)
    bm25_vals = [v.get("bm25", 0.0) for v in by_id.values()]
    vmin, vmax = (min(bm25_vals), max(bm25_vals)) if bm25_vals else (0.0, 1.0)
    for v in by_id.values():
        bm = v.get("bm25", 0.0)
        v["bm25_n"] = (bm - vmin) / (vmax - vmin) if vmax > vmin else 0.0

    # final score
    for v in by_id.values():
        v["score"] = alpha * v["bm25_n"] + (1.0 - alpha) * v.get("vec", 0.0)

    merged = list(by_id.values())
    merged.sort(key=lambda x: x["score"], reverse=True)
    return merged[:top_k]
