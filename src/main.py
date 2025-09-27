from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import health, papers, rag
from .utils.logging import logger

app = FastAPI(title="arxiv-rag-advanced", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(papers.router, prefix="/papers", tags=["papers"])
app.include_router(rag.router, prefix="/rag", tags=["rag"])

@app.on_event("startup")
async def startup():
    logger.info("API started")
