import sys
import os
import hashlib
import logging
import chromadb

#  make project root importable 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    RESUMES_DIR, CHROMA_DIR, CHROMA_COLLECTION,
    OLLAMA_BASE_URL, EMBEDDING_MODEL, SANDBOX_BASE_URL
)
from ingestion.parser import load_all_resumes
from ingestion.nlp_extractor import extract_metadata
from ingestion.embedder import get_embedding

#  logging setup 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ingest.log")
    ]
)
logger = logging.getLogger(__name__)

def make_resume_id(file_name: str) -> str:
    """Generate a stable unique ID from the filename."""
    return "RES-" + hashlib.md5(file_name.encode()).hexdigest()[:8].upper()


def make_sandbox_url(resume_id: str) -> str:
    """Generate a sandbox profile URL for a given resume ID."""
    return f"{SANDBOX_BASE_URL}/{resume_id}"


def already_indexed(collection, resume_id: str) -> bool:
    """Check if this resume is already in ChromaDB (for incremental updates)."""
    result = collection.get(ids=[resume_id])
    return len(result["ids"]) > 0


def run():
    logger.info("=" * 60)
    logger.info("Starting Resume Ingestion Pipeline")
    logger.info("=" * 60)

    #  Step 1: Connect to ChromaDB 
    logger.info(f"Connecting to ChromaDB at: {CHROMA_DIR}")
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        metadata={"hnsw:space": "cosine"}   # cosine similarity for semantic search
    )
    logger.info(f"Collection '{CHROMA_COLLECTION}' ready.")

    #  Step 2: Parse all resumes 
    logger.info(f"Loading resumes from: {RESUMES_DIR}")
    resumes = load_all_resumes(RESUMES_DIR)

    if not resumes:
        logger.error("No resumes found. Check your resumes directory.")
        return

    logger.info(f"Found {len(resumes)} resumes to process.")

    #  Step 3: Process each resume 
    skipped  = 0
    indexed  = 0
    failed   = 0

    for resume in resumes:
        file_name = resume["file_name"]
        text      = resume["text"]

        resume_id   = make_resume_id(file_name)
        sandbox_url = make_sandbox_url(resume_id)

        # Skip if already indexed (incremental support)
        if already_indexed(collection, resume_id):
            logger.info(f"[SKIP] Already indexed: {file_name}")
            skipped += 1
            continue

        # Extract metadata via NLP
        metadata = extract_metadata(text)
        metadata["sandbox_url"]  = sandbox_url
        metadata["file_name"]    = file_name
        metadata["resume_id"]    = resume_id

        # Generate embedding via Ollama
        logger.info(f"[EMBED] Generating embedding for: {file_name}")
        embedding = get_embedding(text[:4000], OLLAMA_BASE_URL, EMBEDDING_MODEL)

        if not embedding:
            logger.error(f"[FAIL] Embedding failed for: {file_name}")
            failed += 1
            continue

        # Upsert into ChromaDB
        collection.upsert(
            ids=[resume_id],
            embeddings=[embedding],
            metadatas=[metadata],
            documents=[text[:2000]]   # store first 2000 chars for keyword fallback
        )

        logger.info(f"[OK] Indexed: {file_name} → {sandbox_url}")
        indexed += 1

    #  Step 4: Summary 
    logger.info("=" * 60)
    logger.info(f"Ingestion Complete!")
    logger.info(f"  Indexed : {indexed}")
    logger.info(f"  Skipped : {skipped} (already in DB)")
    logger.info(f"  Failed  : {failed}")
    logger.info(f"  Total in ChromaDB: {collection.count()}")
    logger.info("=" * 60)


if __name__ == "__main__":
    run()