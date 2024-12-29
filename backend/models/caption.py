from pydantic import BaseModel
from typing import List, Optional


class Caption(BaseModel):            
    ext: Optional[str] = None
    url: Optional[str] = None
    name: Optional[str] = None
