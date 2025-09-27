from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer
from .base import Base, IdMixin

class Paper(Base, IdMixin):
    __tablename__ = "papers"
    arxiv_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(512))
    authors: Mapped[str] = mapped_column(String(1024))
    year: Mapped[int] = mapped_column(Integer)
    abstract: Mapped[str] = mapped_column(Text)

class Chunk(Base, IdMixin):
    __tablename__ = "chunks"
    paper_id: Mapped[int] = mapped_column(Integer, index=True)
    chunk_id: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
