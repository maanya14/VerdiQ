from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

VECTOR_DB_PATH="../vectordb"

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

vectorstore = Chroma(
    persist_directory=VECTOR_DB_PATH,
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

while True:
    query=input("\nAsk a legal question (or type 'exit' to quit): ")
    if query.lower() == 'exit':
        break
    
    docs= retriever.invoke(query)
    print("\nTop Retrieved Documents:\n")

    for i, doc in enumerate(docs,start=1):
        print("="*80)
        print(f"Result {i}")
        print(
            f"Source: {doc.metadata.get('source', 'Unknown')}\n"
        )
        print(
            f"Page: {doc.metadata.get('page', 'Unknown')}\n"
        )
        print()
        print(doc.page_content[:1000])  # Print the first 1000 characters of the document content
        print("\n")