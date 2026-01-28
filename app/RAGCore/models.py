from pydantic import BaseModel
from typing import Optional, Dict

class DocumentUploadRequest(BaseModel):
    filename: str
    content_type: str

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    meta: Optional[Dict] = None
