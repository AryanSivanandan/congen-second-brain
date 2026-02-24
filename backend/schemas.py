from pydantic import BaseModel
from datetime import datetime

class DocumentCreate(BaseModel):
    url: str
    title: str
    byline: str | None = None
    content: str
    excerpt: str | None = None
    word_count: int
    captured_at: datetime