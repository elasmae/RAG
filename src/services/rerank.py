from typing import List
from ..settings import settings

_cross = None

def _lazy_cross():
    global _cross
    if _cross is None:
        from sentence_transformers import CrossEncoder
        _cross = CrossEncoder(settings.cross_encoder_model_name)
    return _cross

def rerank(question: str, candidates: List[dict], top_k: int = 5) -> List[dict]:
    if not candidates:
        return []
    model = _lazy_cross()
    pairs = [(question, c.get("text","")) for c in candidates]
    scores = model.predict(pairs).tolist()
    for c, sc in zip(candidates, scores):
        c["rerank_score"] = float(sc)
    candidates.sort(key=lambda x: x["rerank_score"], reverse=True)
    return candidates[:top_k]
