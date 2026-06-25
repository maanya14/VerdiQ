import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
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

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are an Indian Legal Assistant.
    Use ONLY the provided context to answer.
    Context:{context}
    Question:{question}
    Answer:

    """
)
while True:

    query = input("\nAsk a legal question: ")

    if query.lower() == "exit":
        break

    docs = retriever.invoke(query)
    print("\n===== RETRIEVED DOCUMENTS =====\n")

    for i, doc in enumerate(docs):
        print(f"\n--- Document {i+1} ---")
        print(doc.page_content[:1000])

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    final_prompt = prompt_template.format(
        context=context,
        question=query
    )
    print("\n===== FINAL PROMPT =====\n")
    print(final_prompt[:5000])

    response = llm.invoke(final_prompt)

    print("\nAnswer:\n")
    print(response.content)