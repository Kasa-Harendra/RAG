import os
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import GooglePalmEmbeddings
from langchain.llms import GooglePalm
from langchain.chains import RetrievalQA

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# 1. Load documents (example: load all .txt files in docs/)
docs_path = os.path.join(os.path.dirname(__file__), '../../docs/explanations.md')
loader = TextLoader(docs_path)
documents = loader.load()

# 2. Split documents into chunks
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = splitter.split_documents(documents)

# 3. Create embeddings and vector store
embeddings = GooglePalmEmbeddings(google_api_key=GOOGLE_API_KEY)
vectorstore = FAISS.from_documents(docs, embeddings)

# 4. Set up retriever
retriever = vectorstore.as_retriever()

# 5. Set up LLM
llm = GooglePalm(google_api_key=GOOGLE_API_KEY)

# 6. Build RAG chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

def ask(query):
    return qa_chain.run(query)

if __name__ == "__main__":
    while True:
        query = input("Ask a question (or 'exit'): ")
        if query.lower() == 'exit':
            break
        answer = ask(query)
        print("Answer:", answer)
