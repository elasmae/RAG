#  About this project
A **production-style Retrieval-Augmented Generation (RAG) system** that fetches, indexes, and queries scientific papers from **arXiv**.
It combines **BM25 keyword search**, **dense embeddings (SBERT)**, **hybrid retrieval**, and **cross-encoder re-ranking** to provide accurate answers with references.



## Features 


* Ingestion pipeline for arXiv papers (API + PDF parsing)
* Text chunking + embedding with **Sentence-BERT**
* Hybrid search: **BM25 + dense vectors** in OpenSearch
* Re-ranking with **CrossEncoder**
* FastAPI REST API (`/rag/ask`)
* Gradio demo UI
* Redis cache for answers
* Notebooks for exploration, search, and RAG demo



## Project Structure | Structure du projet

RAG/
├─ src/           # FastAPI app, services, clients
├─ notebooks/     # Exploration & demo notebooks
├─ airflow/       # Ingestion DAGs
├─ Dockerfile
├─ compose.yml
├─ Makefile
├─ pyproject.toml
├─ .env.example
└─ README.md

