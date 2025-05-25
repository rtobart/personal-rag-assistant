from typing import Dict, List
from pydantic import BaseModel

class FileIncoming(BaseModel):
    id: str
    metadata: Dict
    process_configuration: Dict

class FileChunk(BaseModel):
    content: str
    metadata: Dict
    embedding: List[float]