"""
config.py — Central configuration for AI Resume Search Agent.
All values are loaded from the .env file via python-dotenv.
No hardcoded values exist in this file.
To set up: use .env and fill in your values.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

#===============================
#  Load .env from project root 
#===============================
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

def _require(key: str) -> str:
    """Read a required env var. Raises clearly if missing."""
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"\n[CONFIG ERROR] Required environment variable '{key}' is not set.\n"
            f"  → use .env and fill in all values."
        )
    return value

def _optional(key: str, default: str) -> str:
    """Read an optional env var with a fallback default."""
    return os.getenv(key) or default

#========
#  PATHS 
#========
RESUMES_DIR = Path(os.getenv("RESUMES_DIR") or BASE_DIR / "resumes")
CHROMA_DIR  = Path(os.getenv("CHROMA_DIR")  or BASE_DIR / "chroma_db")

#===========
#  CHROMADB 
#===========
CHROMA_COLLECTION: str = _optional("CHROMA_COLLECTION", "resumes")

#==========
#  OLLAMA 
#==========
OLLAMA_BASE_URL:  str = _require("OLLAMA_BASE_URL")
EMBEDDING_MODEL:  str = _require("EMBEDDING_MODEL")
LLM_MODEL:        str = _require("LLM_MODEL")

#==========
#  SANDBOX 
#==========
SANDBOX_BASE_URL: str = _require("SANDBOX_BASE_URL")

#=========
#  SEARCH 
#=========
TOP_K_RESULTS: int = int(_optional("TOP_K_RESULTS", "5"))

#=========
#  API 
#=========
_raw_origins: str = _optional("ALLOWED_ORIGINS", "http://localhost:3000")
ALLOWED_ORIGINS: list[str] = [o.strip() for o in _raw_origins.split(",") if o.strip()]
