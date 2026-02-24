from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from datetime import datetime

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    title = Column(String)
    byline = Column(String, nullable=True)
    content = Column(Text)
    excerpt = Column(Text, nullable=True)
    word_count = Column(Integer)
    content_hash = Column(String, unique=True, index=True)
    captured_at = Column(DateTime, default=datetime.utcnow)