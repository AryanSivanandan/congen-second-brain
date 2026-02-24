from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import hashlib
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal, Base
from models import Document, Chunk
from schemas import DocumentCreate
from services.chunking import paragraph_chunking

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def compute_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()


@app.post("/capture")
def capture_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    content_hash = compute_hash(doc.content)

    existing = db.query(Document).filter(
        Document.content_hash == content_hash
    ).first()

    if existing:
        return {"status": "duplicate", "id": existing.id}

    new_doc = Document(
        url=doc.url,
        title=doc.title,
        byline=doc.byline,
        content=doc.content,
        excerpt=doc.excerpt,
        word_count=doc.word_count,
        content_hash=content_hash,
        captured_at=doc.captured_at
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    
    # Generating Chunks
    chunk_texts = paragraph_chunking(new_doc.content)
    print("Chunk count:", len(chunk_texts))
    
    chunk_objects = []
    for index, chunk_text in enumerate(chunk_texts):
        chunk = Chunk(
            document_id=new_doc.id,
            chunk_index=index,
            content=chunk_text,
            char_length=len(chunk_text)
        )
        chunk_objects.append(chunk)
    db.bulk_save_objects(chunk_objects)
    db.commit()

    return {
        "status": "stored",
        "id": new_doc.id,
        "chunks_created": len(chunk_objects)
    }