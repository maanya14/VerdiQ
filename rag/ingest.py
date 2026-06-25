import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DATA_FOLDER="../data"
VECTOR_STORE_FOLDER="../vectordb"

def load_documents():
    """
    Load documents from the data folder and return a list of documents.
    """
    documents = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(DATA_FOLDER, file)
            print(f"Loading {file}...")
            loader= PyPDFLoader(pdf_path)
            docs= loader.load()
            
            #add source information to each document
            for doc in docs:
                doc.metadata["source"] = file
            documents.extend(docs)
    return documents


def create_chunks(documents):
    """
    Split documents into chunks and return a list of chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


def create_vector_store(chunks):
    """
    Create a vector store from the chunks and return the vector store.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )
    vector_store = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=VECTOR_STORE_FOLDER
    )
    return vector_store

if __name__ == "__main__":
    print("Loading documents...")
    documents = load_documents()
    print(f"Total Pages Loaded: {len(documents)}")
    chunks = create_chunks(documents)
    print(f"Total Chunks Created: {len(chunks)}")
    vector_store = create_vector_store(chunks)
    print("Vector store created")