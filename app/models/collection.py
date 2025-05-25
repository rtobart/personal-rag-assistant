from typing import List, Optional

from pydantic import BaseModel

from app.models.field import Field


class IndexParameters(BaseModel):
    index_type: Optional[str] = "IVF_FLAT"
    metric_type: Optional[str] = "L2"
    params: Optional[dict] = {"nlist": 128}


class CollectionDto(BaseModel):
    name: str
    fields: Optional[List[Field]] = []
    schema_description: Optional[str] = ''
    distance: Optional[str] = ''
    embedding_dimension_size: Optional[int] = None
    index_parameters: Optional[IndexParameters] = None

