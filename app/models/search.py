from app.models.vector import  BaseModel
from typing import Optional, Dict, List
from qdrant_client.models import Distance

class Search(BaseModel):
    top_k: int
    collection_name: str
    search_text: str
    search_embedding: Optional[List[float]]
    filter_property: Optional[str]
    filter_value: Optional[str]
    search_params: Optional[Dict[str, int]] = {"metric": "Cosine",  "k": 10,"ef": 256,"score_threshold": 0.5,"filter": None}