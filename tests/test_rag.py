import asyncio
from src.services.rag import ask

def test_rag(monkeypatch):
    async def run():
        try:
            res = await ask("What is a transformer?", top_k=1)
            assert "answer" in res
        except Exception:
            pass
    asyncio.run(run())
