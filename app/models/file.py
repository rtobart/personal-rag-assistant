from typing import List, Dict
from pydantic import BaseModel


class FileChunk(BaseModel):
    content: str
    metadata: Dict
    embedding: List[float]

class FileBatchBody(BaseModel):
    chunks: List[FileChunk]
    collection: str

class FileBatch(BaseModel):
    file_chunks: List[FileChunk]
