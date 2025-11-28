"""
chroma_store.py

Wrapper around ChromaDB to store and query vector embeddings for MARS.
"""

import os
import chromadb
<<<<<<< HEAD
from chromadb.config import Settings
=======
>>>>>>> ec1bd1a (Upload full local project)
from typing import List, Dict
from datetime import datetime
import uuid


# -----------------------------------------------------------
# 1. Initialize Chroma Client
# -----------------------------------------------------------

def get_chroma_client():
<<<<<<< HEAD
    persist_dir = os.environ.get("CHROMA_PERSIST_DIR", "./chroma_db")

    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=persist_dir
    ))

=======
    """
    Creates a persistent Chroma client.
    """
    # Use the new, recommended PersistentClient
    client = chromadb.PersistentClient(path="./chroma_db")
>>>>>>> ec1bd1a (Upload full local project)
    return client


# -----------------------------------------------------------
# 2. Get or Create Memory Collection
# -----------------------------------------------------------

def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name="mars_memory")


# -----------------------------------------------------------
# 3. UPSERT (Add data to vector DB)
# -----------------------------------------------------------

def upsert_chunk(text: str, embedding: List[float], source: str, user: str = "default") -> str:
    """
    Add a text chunk + embedding to the DB.
    """
    collection = get_collection()

    doc_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    metadata = {
        "source": source,
        "timestamp": timestamp,
        "user": user
    }

    collection.upsert(
        ids=[doc_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata]
    )

    return doc_id


# -----------------------------------------------------------
# 4. QUERY (Retrieve top-k relevant chunks)
# -----------------------------------------------------------

def query_memory(query_embedding: List[float], top_k: int = 5, user: str = "default") -> Dict:
    """
    Query vector DB for similar embeddings.
    """
    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"user": user}
    )

    return results


# -----------------------------------------------------------
# 5. DELETE COLLECTION (Optional cleanup)
# -----------------------------------------------------------

def reset_memory():
    client = get_chroma_client()
    client.delete_collection("mars_memory")
