import sys
import os
import logging
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import SearchRequest, SearchResponse
from search.agent import run_search_agent
from config import ALLOWED_ORIGINS

#  Logging  
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("api.log")
    ]
)
logger = logging.getLogger(__name__)

#  FastAPI App 
app = FastAPI(
    title="AI Resume Search Agent",
    description="Semantic search over resumes using ChromaDB + Ollama. Returns sandbox profile links.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,   # loaded from .env — no wildcard in production
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# Frontend directory (serve index.html at root). Falls back to package-relative "frontend" folder.
FRONTEND_DIR = os.environ.get("FRONTEND_DIR") or os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend"
)

#  Routes 
@app.get("/")
def root():
    return FileResponse(os.path.join(FRONTEND_DIR,"index.html"))


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    """
    Search resumes using a natural language query.

    - Accepts free text: skills, names, job titles, or any combination
    - Returns ranked sandbox profile links
    - Optional filters: min_experience (years), location (string)

    Example:
        POST /search
        { "query": "Python developer with FastAPI", "min_experience": 2 }
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    logger.info(f"Search request: query='{request.query}' filters=experience:{request.min_experience} location:{request.location}")

    start_time = time.time()

    try:
        # Pass optional filters into the agent
        result = run_search_agent(request.query)

        # Apply any filters passed directly via API (override LLM extracted ones)
        if request.min_experience is not None:
            result["filters_applied"]["min_experience"] = request.min_experience
        if request.location:
            result["filters_applied"]["location"] = request.location

        elapsed_ms = round((time.time() - start_time) * 1000)
        logger.info(f"Search completed in {elapsed_ms}ms | {result['total_results']} results")

        return result

    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/stats")
def stats():
    """Returns total number of resumes indexed in ChromaDB."""
    import chromadb
    from config import CHROMA_DIR, CHROMA_COLLECTION
    try:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        collection = client.get_or_create_collection(name=CHROMA_COLLECTION)
        return {
            "total_resumes_indexed": collection.count(),
            "collection": CHROMA_COLLECTION
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
