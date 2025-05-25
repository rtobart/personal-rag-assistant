from typing import List, Dict, Optional
from pydantic import BaseModel

class Document(BaseModel):
    text: str
    metadata: dict

class ProcessMetadata(BaseModel):
    chunking: int
    overlap: int

class Metadata(BaseModel):
    process: ProcessMetadata
    file: Dict

class File(BaseModel):
    metadata: Metadata
    id: str

class Data(BaseModel):
    container_name: str
    timestamp: str
    user: str
    email: str
    business_unit: str
    files: List[File]
    project: str
    app_id: str

class UploadResponse(BaseModel):
    status: str
    message: str
    embedding: str = "gcloud"
    data: Data


class ConfluenceChunk(BaseModel):
    content: str
    metadata: Dict


class ConfluenceInput(BaseModel):
    app_id: str
    chunks: List[ConfluenceChunk]
    chunk_size: int = 100
    chunk_overlap: int = 10
    collection: str = ""
    embedding: str = "azure/text-embedding-ada-002"

class Query(BaseModel):
    query: str
    embedding: str = "gcloud"
    
class FileRequest(BaseModel):
    file_name: str
    space: str
    chunk_size: int = 25
    chunk_overlap: int = 10
    embedding: str = "gcloud"
    
class FileConfluenceDocumentRequest(BaseModel):
    file_name: str
    media_type: str
    download_link: str
    page_origin: str
    space: str
    collection: str
    chunk_token_size: int = 1800
    embedding: str = "gcloud"