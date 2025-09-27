from typing import Iterable

def chunk_text(text: str, max_chars: int = 1200, overlap: int = 120) -> Iterable[str]:
    words = text.split()
    buf: list[str] = []
    size = 0
    for w in words:
        buf.append(w)
        size += len(w) + 1
        if size >= max_chars:
            yield " ".join(buf)
            back = " ".join(buf)[-overlap:].split()
            buf = back
            size = sum(len(x) + 1 for x in buf)
    if buf:
        yield " ".join(buf)
