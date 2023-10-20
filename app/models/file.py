from typing import Optional
from pydantic import BaseModel

from app.models.chunk import ChunkModel


class InputModel(BaseModel):
    url: Optional[str] = None
    type: Optional[str] = None
    chunks: Optional[ChunkModel] = None
