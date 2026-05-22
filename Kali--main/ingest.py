import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DOCS_DIR = "documents"
DB_DIR = "chroma_db"

def ingest_documents():
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        print(f"Created '{DOCS_DIR}' directory. Please put your PDFs inside and run this script again.")
        return

    print("Loading PDFs...")
    loader = PyPDFDirectoryLoader(DOCS_DIR)
    documents = loader.load()

    if not documents:
        print(f"No PDFs found in '{DOCS_DIR}'. Please add some PDFs and run again.")
        return

    print(f"Loaded {len(documents)} pages. Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    print(f"Split into {len(chunks)} chunks. Creating vector database (this might take a minute on first run)...")
    
    # Use lightweight embeddings suitable for local CPU/GPU (all-MiniLM is tiny and fast)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Save to disk
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    
    print(f"Success! Database saved to '{DB_DIR}'.")

if __name__ == "__main__":
    ingest_documents()
