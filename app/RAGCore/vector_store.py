
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

VECTOR_STORE_PATH = "vector.index"
CHUNKS_PATH = "chunks.npy"
META_PATH = "meta.npy"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
model = SentenceTransformer(EMBEDDING_MODEL)

def embed_texts(texts):
	return model.encode(texts, show_progress_bar=False, convert_to_numpy=True)

def save_vector_store(index, chunks, meta):
	faiss.write_index(index, VECTOR_STORE_PATH)
	np.save(CHUNKS_PATH, np.array(chunks, dtype=object))
	np.save(META_PATH, np.array(meta, dtype=object))

def load_vector_store():
	if not os.path.exists(VECTOR_STORE_PATH):
		return None, [], []
	index = faiss.read_index(VECTOR_STORE_PATH)
	chunks = np.load(CHUNKS_PATH, allow_pickle=True).tolist()
	meta = np.load(META_PATH, allow_pickle=True).tolist()
	return index, chunks, meta

def add_chunks_to_store(chunks, meta):
	index, all_chunks, all_meta = load_vector_store()
	embeddings = embed_texts(chunks)
	if index is None:
		dim = embeddings.shape[1]
		index = faiss.IndexFlatL2(dim)
		all_chunks = []
		all_meta = []
	index.add(embeddings)
	all_chunks.extend(chunks)
	all_meta.extend(meta)
	save_vector_store(index, all_chunks, all_meta)

def retrieve_similar_chunks(query, top_k=5):
	index, chunks, meta = load_vector_store()
	if index is None or not chunks:
		return [], {"similarity": 0.0}
	query_emb = embed_texts([query])
	D, I = index.search(query_emb, top_k)
	results = [chunks[i] for i in I[0] if i < len(chunks)]
	scores = [float(1.0 / (1.0 + D[0][j])) for j in range(len(results))]  # similarity
	return results, {"similarity": max(scores) if scores else 0.0}
