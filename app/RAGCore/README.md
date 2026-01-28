# RAG FastAPI System

## Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the API:
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage
- POST `/api/upload` with a PDF or TXT file
- POST `/api/query` with `{ "query": "your question" }`

## Architecture
See `docs/architecture_diagram.png`.

## Explanations
See `docs/explanations.md` for chunk size, retrieval failure, and metrics.
