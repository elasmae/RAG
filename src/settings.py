from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    pg_host: str = "postgres"
    pg_port: int = 5432
    pg_db: str = "arxiv"
    pg_user: str = "arxiv"
    pg_password: str = "arxiv"

    os_host: str = "opensearch"
    os_port: int = 9200
    os_user: str = "admin"
    os_password: str = "admin"
    os_use_ssl: bool = False
    os_index: str = "arxiv_papers"

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0

    ollama_host: str = "ollama"
    ollama_port: int = 11434
    ollama_model: str = "llama3:8b"

    embedding_provider: str = "sbert"  # sbert | hash
    sbert_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    cross_encoder_model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    hybrid_alpha: float = 0.6  # weight for BM25 in fusion

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

settings = Settings()
