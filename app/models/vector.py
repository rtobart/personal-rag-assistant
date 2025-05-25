from pydantic import BaseModel
from typing import Optional, Dict, List

class Vector(BaseModel):
    metadata: Optional[Dict] = None
    embedding: List[float]