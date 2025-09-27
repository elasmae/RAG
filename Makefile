.PHONY: up down logs test fmt lint precommit ingest

up: ; docker compose up -d --build
down: ; docker compose down -v
logs: ; docker compose logs -f --tail=200
test: ; uv run pytest -q
fmt:
	uv run black src tests
	uv run ruff check --fix src tests
lint: ; uv run ruff check src tests
precommit: ; pre-commit install
ingest: ; uv run python -c "from src.services.ingest import ingest; ingest(max_results=2)"
