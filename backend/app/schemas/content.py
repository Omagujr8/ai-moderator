from pydantic import BaseModel
from typing import Optional

class ContentCreate(BaseModel):
    external_id: str
    text: Optional[str] = None
    image_url: Optional[str] = None
    content_type: str
    source_app: str

class ContentResponse(BaseModel):
    id: int
    status: str

    class Config:
        from_attributes = True
