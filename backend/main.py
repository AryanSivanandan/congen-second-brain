from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import hashlib
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal, Base
from models import Document, Chunk
from schemas import DocumentCreate, QueryRequest, QueryResponse
from services.chunking import paragraph_chunking
from services.embedding import embed_query, embed_text
import json 
from sklearn.metrics.pairwise import cosine_similarity

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

@app.post("/query")
def query_memory(req: QueryRequest, db: Session = Depends(get_db)):

    query_embedding = embed_query(req.query)

    chunks = db.query(Chunk).all()

    results = []

    for chunk in chunks:

        chunk_embedding = json.loads(chunk.embedding)

        similarity = cosine_similarity(
            [query_embedding],
            [chunk_embedding]
        )[0][0]

        results.append({
            "chunk": chunk.content,
            "similarity": similarity
        })

    results.sort(key=lambda x: x["similarity"], reverse=True)

    return results[:5]

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

        embedding = embed_text(chunk_text)

        chunk = Chunk(
            document_id=new_doc.id,
            chunk_index=index,
            content=chunk_text,
            embedding=json.dumps(embedding),
            char_length=len(chunk_text)
        )
        chunk_objects.append(chunk)
    
    for c in chunk_objects:
        db.add(c)

    db.commit()

    return {
        "status": "stored",
        "id": new_doc.id,
        "chunks_created": len(chunk_objects)
    }