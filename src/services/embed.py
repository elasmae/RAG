from typing import List
import hashlib
from ..settings import settings

_sbert_model = None

def _lazy_sbert():
    global _sbert_model
    if _sbert_model is None:
        from sentence_transformers import SentenceTransformer
        _sbert_model = SentenceTransformer(settings.sbert_model_name)
    return _sbert_model

def embed_texts(texts: List[str]) -> List[List[float]]:
    provider = settings.embedding_provider.lower()
    if provider == "sbert":
        model = _lazy_sbert()
        arr = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
        return arr.tolist()
    # hash embeddings 8-dim
    vecs: List[List[float]] = []
    for t in texts:
        h = hashlib.sha256(t.encode()).digest()[:32]
        nums = [int.from_bytes(h[i:i+4], "big") / 2**32 for i in range(0, 32, 4)]
        vecs.append(nums)
    return vecs

def embed_query(text: str) -> List[float]:
    return embed_texts([text])[0]
