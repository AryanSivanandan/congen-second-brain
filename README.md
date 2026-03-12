# Congen Second Brain


![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-green)
![License](https://img.shields.io/badge/license-MIT-orange)

Congen Second Brain is a local-first semantic knowledge system that captures web content, converts it into structured chunks, generates embeddings, and enables meaning-based search over your personal research archive.

The system turns saved articles into a searchable memory engine that can retrieve information based on semantic similarity rather than keywords.

---

## Key Capabilities

- Browser-based article capture
- Automatic document ingestion
- Paragraph-based semantic chunking
- Embedding generation using BGE-small
- Vector similarity search over stored knowledge
- Local-first architecture

---

## Example Semantic Query

Query:

```
types of cats
```

Result:

```
Canada lynx
Eurasian lynx
Iberian lynx
Cheetah
Jaguarundi
Cougar
Leopard cat lineage
Domestic cat lineage
```

The system retrieves semantically relevant knowledge rather than exact keyword matches.

---

## Quickstart

Clone the repository:

```
git clone https://github.com/your-username/congen-second-brain.git
cd congen-second-brain/backend
```

Create a virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```
pip install fastapi uvicorn sqlalchemy pydantic nltk python-multipart sentence-transformers numpy
```

Run the backend:

```
uvicorn main:app --reload
```

Open the API docs:

```
http://127.0.0.1:8000/docs
```

---

The system currently consists of:

- A Firefox browser extension for article capture
- A FastAPI backend for ingestion
- A relational database layer (SQLite)
- Deterministic paragraph-based chunking
- Semantic embedding generation
- Vector-based similarity retrieval

The goal of the project is to build the foundation for a personal AI knowledge system capable of semantic retrieval, topic linking, and long-term research memory.

---

# Features

## Browser-Based Article Capture

The Firefox extension enables capturing long-form web content directly from the browser.

Capabilities include:

- Full-page extraction using Mozilla Readability
- Keyboard shortcut based capture
- Structured JSON payload generation
- Basic content validation before ingestion

Captured articles are sent to the backend ingestion API.

---

## Backend Ingestion API

The backend service is built with FastAPI and processes captured articles.

Key functionality:

- `/capture` endpoint for ingestion
- SHA-256 content hashing for duplicate detection
- Schema validation using Pydantic
- CORS configuration for browser extension communication

Captured documents are stored and automatically processed for chunking and embedding.

---

## Deterministic Paragraph Chunking

Articles are split into structured chunks before embedding.

Chunking strategy:

- Paragraph-based segmentation
- Sentence fallback for oversized paragraphs
- Maximum character threshold per chunk
- Deterministic chunk ordering
- Unique `(document_id, chunk_index)` constraint

This produces semantically meaningful text segments suitable for embedding.

---

## Semantic Embedding Layer

Each chunk is converted into a semantic vector representation using the model:

`BAAI/bge-small-en-v1.5`

Embeddings allow the system to perform semantic search rather than relying on keyword matching.

Each chunk stores:

- chunk text
- metadata
- embedding vector

---

## Semantic Retrieval API

The backend exposes a semantic query endpoint.

```
POST /query
```

Query workflow:

```
User query
    ↓
Query embedding generation
    ↓
Cosine similarity against stored chunk embeddings
    ↓
Rank results
    ↓
Return top relevant chunks
```

This enables knowledge retrieval based on meaning rather than exact words.

---

# Architecture

```
Firefox Extension
        ↓
Background Script
        ↓
POST /capture
        ↓
FastAPI Backend
        ↓
Document Storage (SQLite)
        ↓
Paragraph Chunking
        ↓
Embedding Generation
        ↓
Chunk + Vector Storage
        ↓
Semantic Query (/query)
```

---

# Project Structure

```
congen-second-brain/
│
├── extension/
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   ├── popup.js
│   ├── popup.html
│   └── libs/
│       └── readability.js
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── services/
│   │   ├── chunking.py
│   │   └── embedding.py
│
├── .gitignore
└── README.md
```

---

# Database Schema

## documents

| Field | Type | Notes |
|------|------|------|
| id | Integer | Primary key |
| url | String | Indexed |
| title | String | |
| byline | String | Nullable |
| content | Text | Raw article |
| excerpt | Text | Nullable |
| word_count | Integer | |
| content_hash | String | Unique deduplication |
| captured_at | DateTime | |

---

## chunks

| Field | Type | Notes |
|------|------|------|
| id | Integer | Primary key |
| document_id | Integer | Foreign key |
| chunk_index | Integer | Order within document |
| content | Text | Chunk text |
| char_length | Integer | Length metadata |
| embedding | Text | Vector embedding |
| created_at | DateTime | Timestamp |

Constraint:

```
Unique(document_id, chunk_index)
```

---

# Setup

## Clone Repository

```
git clone https://github.com/your-username/congen-second-brain.git
cd congen-second-brain/backend
```

---

## Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

---

## Install Dependencies

```
pip install fastapi uvicorn sqlalchemy pydantic nltk python-multipart sentence-transformers numpy
```

---

## Download NLTK Tokenizer

Start Python:

```
python
```

Then run:

```
import nltk
nltk.download('punkt')
```

Exit Python.

---

## Run Backend

```
uvicorn main:app --reload
```

Backend will run at:

```
http://127.0.0.1:8000
```

Swagger documentation is available at:

```
http://127.0.0.1:8000/docs
```

---

# Loading the Firefox Extension

1. Open:

```
about:debugging
```

2. Click:

```
Load Temporary Add-on
```

3. Select:

```
extension/manifest.json
```

---

# Usage

Press:

```
Ctrl + Shift + Y
```

The system will:

1. Extract article content
2. Send data to backend
3. Store the document
4. Generate chunks
5. Create embeddings
6. Persist semantic vectors

---

# Querying Stored Knowledge

Example request:

```
POST /query
```

```
{
  "query": "types of cats"
}
```

The system returns the most semantically relevant stored chunks.

---

# Verifying Storage

You can inspect stored data using DB Browser for SQLite.

Open:

```
backend/second_brain.db
```

Verify:

- `documents` table contains captured articles
- `chunks` table contains chunked segments
- embeddings are stored for each chunk

---

# Design Principles

The system is designed around the following principles:

- Deterministic chunking
- Clear separation of concerns
- Service-layer architecture
- Relational normalization
- Extensibility-first design

Chunking logic is isolated inside:

```
backend/services/chunking.py
```

Embedding logic is implemented inside:

```
backend/services/embedding.py
```

---

# Current Status

The following pipeline is fully implemented:

- Article capture via browser extension
- Backend ingestion
- Duplicate detection
- Deterministic paragraph chunking
- Embedding generation
- Semantic similarity search

The system now functions as a **local semantic research memory engine**.

---

# Future Work

Planned improvements include:

- Vector indexing (FAISS or HNSW)
- Topic clustering
- Knowledge graph construction
- Cross-document summarization
- Multi-device synchronization
- AI-assisted research queries