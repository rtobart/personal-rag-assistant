from pydantic import BaseModel

class InputModel(BaseModel):
    text: str
    embeddingAlgorithm: str
    vectorsTopK: int
    llmAgentDescription: str

class OutputModel(BaseModel):
    answer: str
