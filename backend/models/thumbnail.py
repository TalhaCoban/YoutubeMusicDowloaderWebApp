from pydantic import BaseModel
from typing import Optional, List


class Thumbnail(BaseModel):
    url: Optional[str] = None
    preference: Optional[int] = None
    id: Optional[str] = None