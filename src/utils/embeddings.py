"""
embeddings.py

Utility module to generate text embeddings using SentenceTransformers.
This will be used by Research Agent, Knowledge Agent, Summary Agent, etc.
"""

from sentence_transformers import SentenceTransformer
from functools import lru_cache
from typing import List, Union

# -------------------------------------
# Load embedding model using caching
# -------------------------------------
@lru_cache(maxsize=1)
def load_embedding_model(model_name: str = "all-MiniLM-L6-v2"):
    """
    Loads and caches the embedding model.
    Using a small model for faster embedding generation.
    """
    model = SentenceTransformer(model_name)
    return model


# -------------------------------------
# Embedding function
# -------------------------------------
def embed_text(text: Union[str, List[str]]) -> List[List[float]]:
    """
    Generate embeddings for either a single string or list of strings.

    Args:
        text (str or list[str]): Input text(s) to embed.

    Returns:
        List[List[float]]: Embedding vectors
    """
    model = load_embedding_model()

    if isinstance(text, str):
        text = [text]

    embeddings = model.encode(text, convert_to_numpy=True)

    return embeddings.tolist()
