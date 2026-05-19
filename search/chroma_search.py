import sys
import os
import logging
import chromadb

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    CHROMA_DIR, CHROMA_COLLECTION,
    OLLAMA_BASE_URL, EMBEDDING_MODEL, TOP_K_RESULTS
)
from ingestion.embedder import get_embedding

logger = logging.getLogger(__name__)


def get_collection():
    """Connect to ChromaDB and return the resumes collection."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        metadata={"hnsw:space": "cosine"}
    )


def build_where_filter(filters: dict) -> dict | None:
    """
    Build a ChromaDB where= filter from optional search filters.

    Supported filters:
        min_experience: int  → experience_years >= value
        location:       str  → exact location match
        skill:          str  → skills field contains value
    """
    conditions = []

    if filters.get("min_experience"):
        conditions.append({"experience_years": {"$gte": int(filters["min_experience"])}})

    if filters.get("location"):
        conditions.append({"location": {"$eq": filters["location"]}})

    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"$and": conditions}


def search_resumes(query: str, filters: dict = {}) -> list[dict]:
    """
    Perform semantic search over ChromaDB.

    Args:
        query:   Natural language search query
        filters: Optional dict with keys: min_experience, location

    Returns:
        List of result dicts with sandbox_link, score, skills, etc.
    """
    collection = get_collection()

    # Check collection has data
    total = collection.count()
    if total == 0:
        logger.warning("ChromaDB collection is empty. Run ingestion first.")
        return []

    # Embed the query using the same model as ingestion
    logger.info(f"Embedding query: '{query}'")
    query_embedding = get_embedding(query, OLLAMA_BASE_URL, EMBEDDING_MODEL)

    if not query_embedding:
        logger.error("Failed to embed query. Is Ollama running?")
        return []

    # Build optional metadata filter
    where_filter = build_where_filter(filters)

    # Query ChromaDB
    query_params = {
        "query_embeddings": [query_embedding],
        "n_results":        min(TOP_K_RESULTS, total),
        "include":          ["metadatas", "distances", "documents"]
    }
    if where_filter:
        query_params["where"] = where_filter

    results = collection.query(**query_params)

    # Format results
    formatted = []
    for i, metadata in enumerate(results["metadatas"][0]):
        distance = results["distances"][0][i]
        # Convert cosine distance → similarity score (0.0–1.0)
        score = round(1 - distance, 4)

        formatted.append({
            "rank":             i + 1,
            "similarity_score": score,
            "sandbox_link":     metadata.get("sandbox_url", "N/A"),
            "candidate_name":   metadata.get("candidate_name", "Unknown"),
            "matched_skills":   metadata.get("skills", "").split(", "),
            "experience_years": metadata.get("experience_years", 0),
            "location":         metadata.get("location", "Unknown"),
            "file_name":        metadata.get("file_name", ""),
        })

    logger.info(f"Search returned {len(formatted)} results for query: '{query}'")
    return formatted