from fastapi import APIRouter
from pydantic import BaseModel
from ..services.rag import ask

class RAGQuery(BaseModel):
    question: str
    top_k: int = 5

router = APIRouter()

@router.post("/ask")
async def rag_ask(q: RAGQuery):
    return await ask(q.question, q.top_k)

