from langchain_core.output_parsers import PydanticOutputParser

from schemas import ContractClause

parser = PydanticOutputParser(
    pydantic_object=ContractClause
)