from typing import Dict
from ..clients.ollama import complete
from ..clients.redis_client import get_redis
from .hybrid_search import hybrid_search
from .rerank import rerank
import json

def _cache_key(q: str) -> str:
    return f"rag:ans:{q}"

async def ask(question: str, top_k: int = 5) -> Dict:
    r = get_redis()
    key = _cache_key(question)
    cached = r.get(key)
    if cached:
        return json.loads(cached.decode())

    # 1) retrieval hybride
    candidates = hybrid_search(question, bm25_k=20, vec_k=20, top_k=20)

    # 2) re-ranking
    ranked = rerank(question, candidates, top_k=max(top_k, 5))

    # 3) composer le contexte
    context = "\n\n".join(d.get("text","") for d in ranked)

    # 4) prompt
    prompt = (
        "Vous êtes un assistant de recherche. Utilisez UNIQUEMENT le CONTEXTE pour répondre de manière concise; "
        "si l'information manque, dites \"Je ne sais pas\". Citez les titres entre crochets [].\n\n"
        f"CONTEXTE:\n{context}\n\nQUESTION: {question}\nRÉPONSE:"
    )

    answer = await complete(prompt)
    sources = [{"title": d["title"], "score": d.get("rerank_score", d.get("score", 0.0))} for d in ranked[:top_k]]
    result = {"answer": answer, "sources": sources}

    r.set(key, json.dumps(result), ex=3600)
    return result
