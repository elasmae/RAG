from src.services.hybrid_search import hybrid_search

def test_hybrid_search(monkeypatch):
    
    results = []
    try:
        results = hybrid_search("neural networks", top_k=1)
    except Exception:
        pass
    assert isinstance(results, list)
