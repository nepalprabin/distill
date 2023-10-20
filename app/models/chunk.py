from pydantic import BaseModel
from typing import Optional


class ChunkModel(BaseModel):
    chunk_size: Optional[int] = None
    chunk_overlap: Optional[int] = None
