from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from .models import DocumentUploadRequest, QueryRequest, QueryResponse
from .rag import ingest_document, answer_query
from .rate_limiter import rate_limiter

app = FastAPI()

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    background_tasks.add_task(ingest_document, file)
    return {"status": "Ingestion started"}

@app.post("/api/query", response_model=QueryResponse)
async def query_api(request: QueryRequest, rl=Depends(rate_limiter)):
    answer, meta = answer_query(request.query)
    return QueryResponse(answer=answer, meta=meta)
