from src.services.ingest import fetch_arxiv

def test_fetch_arxiv():
    papers = fetch_arxiv("cs.CL", max_results=1)
    assert len(papers) > 0
    assert "title" in papers[0]
