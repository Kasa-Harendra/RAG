from pydantic import BaseModel
from typing import Optional

class UploadResponse(BaseModel):
    message: str

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    error: Optional[str] = None
