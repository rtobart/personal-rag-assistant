from pydantic import BaseModel

class InputModel(BaseModel):
    text: str
    embeddingAlgorithm: str
    vectorsTopK: int
    llmAgentDescription: str
    modelProvider: str

class InputBulkModel(BaseModel):
    collection_name: str
    embedding_algorithm: str

class OutputModel(BaseModel):
    answer: str
