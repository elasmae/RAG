import httpx
from ..settings import settings

async def complete(prompt: str) -> str:
    url = f"http://{settings.ollama_host}:{settings.ollama_port}/api/generate"
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(url, json={"model": settings.ollama_model, "prompt": prompt})
        r.raise_for_status()
        data = r.json()
        return data.get("response", "")
