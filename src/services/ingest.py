import io, re, requests
from typing import List
from sqlalchemy.orm import Session
from pypdf import PdfReader
from ..clients.postgres import engine, SessionLocal
from ..models.base import Base
from ..models.paper import Paper, Chunk
from .chunk import chunk_text
from .embed import embed_texts
from .hybrid_search import ensure_index, index_chunk

ARXIV_API = "http://export.arxiv.org/api/query"

def init_db():
    Base.metadata.create_all(bind=engine)

def fetch_arxiv(category: str = "cs.CL", max_results: int = 2) -> List[dict]:
    q = {"search_query": f"cat:{category}", "start": 0, "max_results": max_results,
         "sortBy": "submittedDate", "sortOrder": "descending"}
    r = requests.get(ARXIV_API, params=q, timeout=30)
    r.raise_for_status()
    text = r.text
    entries = text.split("<entry>")[1:]
    out = []
    for e in entries:
        aid = re.search(r"<id>(.*?)</id>", e)
        title = re.search(r"<title>(.*?)</title>", e, flags=re.S)
        summary = re.search(r"<summary>(.*?)</summary>", e, flags=re.S)
        pdf = re.search(r'href="(http.*?pdf)"', e)
        authors = ", ".join(re.findall(r"<name>(.*?)</name>", e))
        if aid and title and summary:
            out.append({
                "arxiv_id": aid.group(1).split("/abs/")[-1],
                "title": re.sub(r"\s+", " ", title.group(1)).strip(),
                "abstract": re.sub(r"\s+", " ", summary.group(1)).strip(),
                "authors": authors,
                "pdf_url": pdf.group(1) if pdf else None,
            })
    return out

def download_pdf(url: str) -> bytes:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.content

def parse_pdf(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    texts = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(texts)

def ingest(category: str = "cs.CL", max_results: int = 2):
    init_db()
    ensure_index()
    items = fetch_arxiv(category=category, max_results=max_results)
    with SessionLocal() as s:
        for it in items:
            paper = s.query(Paper).filter(Paper.arxiv_id == it["arxiv_id"]).one_or_none()
            if not paper:
                paper = Paper(
                    arxiv_id=it["arxiv_id"],
                    title=it["title"],
                    authors=it.get("authors",""),
                    year=2025,
                    abstract=it["abstract"],
                )
                s.add(paper)
                s.flush()
            full_text = it["abstract"]
            if it.get("pdf_url"):
                try:
                    pdf = download_pdf(it["pdf_url"])
                    full_text = parse_pdf(pdf) or full_text
                except Exception:
                    pass
            chunks = list(chunk_text(full_text))
            for i, ch in enumerate(chunks):
                s.add(Chunk(paper_id=paper.id, chunk_id=i, text=ch))
            s.commit()
            vecs = embed_texts(chunks)
            for i, ch in enumerate(chunks):
                doc = {
                    "doc_id": f"{paper.id}:{i}",
                    "paper_id": paper.id,
                    "chunk_id": i,
                    "title": paper.title,
                    "abstract": paper.abstract,
                    "text": ch,
                    "vector": vecs[i],
                }
                index_chunk(doc)
