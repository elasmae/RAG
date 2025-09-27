from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..settings import settings

engine = create_engine(
    f"postgresql+psycopg2://{settings.pg_user}:{settings.pg_password}"
    f"@{settings.pg_host}:{settings.pg_port}/{settings.pg_db}",
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
