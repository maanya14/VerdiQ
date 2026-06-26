from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from torch import embedding

pdf_path = "../../data/Contract Act.pdf"

loader = PyPDFLoader(pdf_path)
documents = loader.load()
print("Pages loaded:", len(documents))

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)
print("Chunks:", len(chunks))

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)
print(chunks[0].page_content[:200])

test_embedding = embeddings.embed_query("Hello world")

print(type(test_embedding))
print(len(test_embedding))
print(test_embedding[:5])
db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="../../legal_db"
)

print("Legal database created")