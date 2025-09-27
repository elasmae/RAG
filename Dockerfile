FROM python:3.12-slim
WORKDIR /app

# System deps useful for sentence-transformers and git resolution
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv
COPY pyproject.toml ./
RUN uv sync --no-dev --frozen

COPY src ./src
COPY .env.example ./
ENV PYTHONUNBUFFERED=1
EXPOSE 8000 7861
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
