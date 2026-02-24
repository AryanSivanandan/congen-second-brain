Congen Second Brain

Congen Second Brain is a local-first research capture and semantic ingestion system designed to transform web content into structured, retrieval-ready memory.

The system consists of:

A Firefox browser extension for article capture

A FastAPI backend for ingestion

A relational database layer (SQLite)

Deterministic paragraph-based chunking

Structured chunk persistence

It serves as a foundational layer for future embedding and semantic retrieval functionality.

Current Features
Browser-Based Article Capture

Full-page extraction using Mozilla Readability

Keyboard shortcut support

Structured JSON payload generation

Basic content quality validation (length-based)

Backend Ingestion API

FastAPI-based /capture endpoint

SHA-256 content hashing for duplicate detection

Schema validation using Pydantic

CORS configuration for extension communication

Relational Persistence Layer

SQLite database

Normalized documents table

Separate chunks table

Proper foreign key relationships

Cascade deletion support

Deterministic chunk indexing

Paragraph-Based Chunking

Splits content at paragraph boundaries

Fallback to sentence splitting for oversized paragraphs

Fixed maximum chunk size

Stable deterministic ordering

Stored per document with unique (document_id, chunk_index) constraint

Architecture
Firefox Extension
        ↓
Background Script
        ↓
POST /capture
        ↓
Document Storage (SQLite)
        ↓
Paragraph Chunking Service
        ↓
Chunk Storage (Relational)
Project Structure
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
│   │   └── chunking.py
│   └── venv/
│
└── README.md
Database Schema
documents Table
Field	Type	Notes
id	Integer	Primary key
url	String	Indexed
title	String	
byline	String	Nullable
content	Text	Full raw article
excerpt	Text	Nullable
word_count	Integer	
content_hash	String	Unique, used for deduplication
captured_at	DateTime	
chunks Table
Field	Type	Notes
id	Integer	Primary key
document_id	Integer	Foreign key → documents.id
chunk_index	Integer	Order preserved
content	Text	Chunk text
char_length	Integer	Length metadata
created_at	DateTime	Timestamp

Constraint:

Unique(document_id, chunk_index)
Setup Instructions
1. Clone Repository
git clone https://github.com/your-username/congen-second-brain.git
cd congen-second-brain/backend
2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate
3. Install Dependencies
pip install fastapi uvicorn sqlalchemy pydantic nltk python-multipart
4. Download NLTK Tokenizer

Start Python:

python

Then run:

import nltk
nltk.download('punkt')

Exit Python.

5. Run Backend
uvicorn main:app --reload

Backend runs at:

http://127.0.0.1:8000

Swagger documentation is available at:

http://127.0.0.1:8000/docs
Loading the Firefox Extension

Open:

about:debugging

Click Load Temporary Add-on

Select manifest.json inside the extension/ directory

Usage

Press:

Ctrl + Shift + Y

The system will:

Extract article content

Send data to backend

Store the document

Generate paragraph-based chunks

Persist chunks to the database

Verifying Storage

Use DB Browser for SQLite.

Open:

backend/second_brain.db

Verify:

documents table is populated

chunks table contains multiple rows per document

chunk_index increments sequentially

Design Principles

This system follows:

Deterministic chunking

Clear separation of concerns

Service-layer architecture

Relational normalization

Extensibility-first design

Chunking logic is isolated in:

services/chunking.py

The backend is structured to remain independent of future embedding or vector layers.

Why Chunking Matters

Embedding models operate more effectively on smaller semantic units rather than full documents.

Instead of embedding entire articles, this system:

Segments content into paragraph-aware chunks

Preserves chunk order using chunk_index

Prepares each chunk for future vector embedding

This enables:

Fine-grained semantic retrieval

Improved RAG performance

Efficient indexing strategies

Planned Next Steps

Embedding generation per chunk

Vector storage integration

Semantic retrieval endpoint

Query-based RAG interface

Local-first embedding provider support

Current Status

End-to-end ingestion working

Deduplication implemented

Chunk persistence verified

Stable relational structure

The system is now prepared for embedding layer integration.
