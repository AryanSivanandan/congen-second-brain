from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
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

    chunks = relationship(
        "Chunk",
        back_populates="document",
        cascade="all, delete-orphan"
    )


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )

    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    char_length = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("document_id", "chunk_index", name="uix_doc_chunk_index"),
    )

    document = relationship("Document", back_populates="chunks")