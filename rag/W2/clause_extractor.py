from rag.W2.parser import parser
import json
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from rag.W2.prompts import CLAUSE_EXTRACTION_PROMPT
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

pdf_path="../../data/Rental Agreement 2.pdf"
loader = PyPDFLoader(pdf_path)
docs= loader.load()

contract_text = "\n\n".join(
    [doc.page_content for doc in docs]
)

prompt=CLAUSE_EXTRACTION_PROMPT.format(
    contract_text=contract_text,    
    format_instructions=parser.get_format_instructions()
)

response = llm.invoke(prompt)
result = parser.parse(response.content)
print(result)
output_path="../outputs/rental_agreement_2_clauses.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(
        result.model_dump(), 
        f, 
        ensure_ascii=False, 
        indent=4
    )

print(f"Saved to {output_path}")    