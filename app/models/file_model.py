from typing import Optional
from pydantic import BaseModel


class InputModel(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None
    type: Optional[str] = None
