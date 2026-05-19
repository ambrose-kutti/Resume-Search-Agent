import sys
import os
import json
import logging
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OLLAMA_BASE_URL, LLM_MODEL
from search.chroma_search import search_resumes

logger = logging.getLogger(__name__)

def query_ollama_llm(prompt: str) -> str:
    """
    Send a prompt to Ollama LLM and return the response text.
    Uses the /api/generate endpoint directly for simplicity.
    """
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model":  LLM_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Ollama. Make sure it is running.")
        return ""
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return ""


def extract_search_intent(user_query: str) -> dict:
    """
    Use the Ollama LLM to extract structured search intent from a natural
    language query.

    Returns a dict with:
        search_query:   cleaned/expanded query to embed
        min_experience: int or null
        location:       string or null
        explanation:    what the LLM understood
    """
    prompt = f"""You are a resume search assistant. A user has typed a search query.
Extract the structured search intent from it.

User query: "{user_query}"

Respond ONLY with a valid JSON object — no explanation, no markdown, no extra text.
Use this exact format:
{{
  "search_query": "the core search phrase to use for semantic search",
  "min_experience": null or integer (years),
  "location": null or "city/country string",
  "explanation": "one sentence describing what the user is looking for"
}}

Rules:
- search_query should be the most useful phrase for finding matching resumes
- If no experience or location is mentioned, set those fields to null
- Do not add fields that are not in the format above
"""

    logger.info("Calling LLM for query understanding...")
    raw = query_ollama_llm(prompt)

    # Parse JSON from LLM response
    try:
        # Strip any accidental markdown fences
        clean = raw.strip().strip("```json").strip("```").strip()
        intent = json.loads(clean)
        logger.info(f"Extracted intent: {intent}")
        return intent
    except json.JSONDecodeError:
        logger.warning(f"LLM returned non-JSON: {raw}. Falling back to raw query.")
        return {
            "search_query":   user_query,
            "min_experience": None,
            "location":       None,
            "explanation":    "Direct search (LLM parse failed)"
        }


def run_search_agent(user_query: str) -> dict:
    """
    Full agent pipeline:
    1. LLM understands and expands the query
    2. ChromaDB semantic search with extracted filters
    3. Returns structured response with sandbox links

    Args:
        user_query: Raw natural language input from the user

    Returns:
        Dict with query metadata, LLM explanation, and ranked results
    """
    logger.info(f"Agent received query: '{user_query}'")

    # Step 1: LLM query understanding
    intent = extract_search_intent(user_query)

    search_query   = intent.get("search_query", user_query)
    min_experience = intent.get("min_experience")
    location       = intent.get("location")
    explanation    = intent.get("explanation", "")

    # Build filters dict
    filters = {}
    if min_experience:
        filters["min_experience"] = min_experience
    if location:
        filters["location"] = location

    # Step 2: Semantic search in ChromaDB
    results = search_resumes(search_query, filters)

    # Step 3: Return structured response
    return {
        "original_query":  user_query,
        "understood_as":   explanation,
        "search_query":    search_query,
        "filters_applied": filters,
        "total_results":   len(results),
        "results":         results
    }