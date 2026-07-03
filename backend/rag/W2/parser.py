from langchain_core.output_parsers import PydanticOutputParser

from rag.W2.schemas import ContractClause

parser = PydanticOutputParser(
    pydantic_object=ContractClause
)