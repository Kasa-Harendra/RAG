from .utils import parse_file, chunk_text
from .vector_store import add_chunks_to_store

def ingest_document(file):
    content = parse_file(file)
    chunks = chunk_text(content, chunk_size=500)
    meta = [{"filename": file.filename}] * len(chunks)
    add_chunks_to_store(chunks, meta)

from .vector_store import retrieve_similar_chunks
from .google_llm import generate_answer

def answer_query(query):
    chunks, meta = retrieve_similar_chunks(query)
    answer = generate_answer(query, chunks)
    return answer, meta
