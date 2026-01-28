from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import GooglePalm
from langchain.chains import RetrievalQA
import threading

app = FastAPI()

# Allow CORS for all origins (customize as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
INDEX_PATH = os.path.join(os.path.dirname(__file__), 'vector.index')

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Global objects (thread-safe for demo, use better state management in prod)
vectorstore = None
retriever = None
qa_chain = None

# Helper: Preprocess and index file
def preprocess_and_index(file_path):
    global vectorstore, retriever, qa_chain
    loader = TextLoader(file_path)
    documents = loader.load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.split_documents(documents)
    # Use local HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(INDEX_PATH)
    retriever = vectorstore.as_retriever()
    llm = GooglePalm(google_api_key=GOOGLE_API_KEY)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Helper: Load index if exists
def load_index():
    global vectorstore, retriever, qa_chain
    if os.path.exists(INDEX_PATH):
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(INDEX_PATH, embeddings)
        retriever = vectorstore.as_retriever()
        llm = GooglePalm(google_api_key=GOOGLE_API_KEY)
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

load_index()

@app.post("/api/upload")
def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    background_tasks.add_task(preprocess_and_index, file_path)
    return {"message": "File uploaded. Indexing started in background."}

@app.post("/api/query")
def query_rag(query: str = Form(...)):
    if qa_chain is None:
        return JSONResponse(status_code=503, content={"error": "Index not ready. Please upload and wait for indexing."})
    answer = qa_chain.run(query)
    return {"answer": answer}

@app.get("/")
def root():
    return {"message": "LangChain RAG FastAPI server running."}
