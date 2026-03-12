from sentence_transformers import SentenceTransformer
import numpy as np 
## IMPORTANT!! Model must only be initialized once and not multiple times
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def embed_text(text: str):
    embedding = model.encode(text)
    return embedding.tolist()

def embed_query(query: str):
    query = "query:" + query 
    embedding = model.encode(query)
    return embedding.tolist()