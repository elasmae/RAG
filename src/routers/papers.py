from fastapi import APIRouter, Query
from typing import List, Dict

router = APIRouter()

@router.get("/", response_model=List[Dict])
def list_papers(q: str | None = Query(default=None)):
    # TODO: implémenter une requête Postgres/OS si besoin
    return []
