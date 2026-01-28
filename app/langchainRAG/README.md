# langchainRAG

This is a Retrieval-Augmented Generation (RAG) system implemented using the LangChain framework. It provides similar functionality to the custom RAGCore system, but leverages LangChain's modular components for document loading, vector storage, retrieval, and LLM integration.

- **Framework:** LangChain
- **Vector Store:** FAISS
- **LLM:** Google Palm (or any LLM supported by LangChain)
- **Embeddings:** HuggingFaceEmbeddings

## Features
- Uses LangChain for document ingestion, vectorization, and retrieval
- Integrates with Google LLM (or other LLMs supported by LangChain)
- Easily extensible with LangChain's tools and chains
- FastAPI server for file upload, background indexing, and querying

## How it Works

1. **Document Loading:** User uploads a document.
2. **Chunking:** Splits documents into manageable text chunks.
3. **Embedding & Indexing:** Converts chunks to embeddings and stores them in a FAISS vector store.
4. **Retrieval:** Retrieves relevant chunks for a user query.
5. **Generation:** Uses an LLM to generate answers based on retrieved context.

## Setup
1. **Clone the repository** and navigate to the `langchainRAG` directory.
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Copy `.env` and add your Google API key:
     ```env
     GOOGLE_API_KEY=your_google_api_key_here
     ```

## Running the App

### Start the FastAPI server
```bash
uvicorn app:app --reload
```

### API Endpoints
- `POST /api/upload` — Upload a file for background preprocessing and indexing (form field: `file`)
- `POST /api/query` — Query the indexed documents (form field: `query`)
- `GET /` — Health check

## Usage (CLI)

You can also run the app from the command line:
```bash
python main.py
```

## About
This implementation is provided as a reference for building RAG systems with LangChain. For a custom, framework-free version, see the `RAGCore` directory in this repository.

---

For a custom, framework-free RAG implementation, see the `RAGCore` directory.
