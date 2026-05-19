"""
nlp_extractor.py — Production-grade metadata extraction for resumes.

Strategy:
  - Candidate name   → spaCy NER (fast, no LLM cost)
  - Location         → spaCy NER (fast, no LLM cost)
  - Experience years → regex patterns (fast, deterministic)
  - Skills           → Ollama LLM (no hardcoded list; extracts any skill
                       the LLM recognises from the resume text itself)

This approach requires zero maintenance — no skills list to update
as new technologies emerge.
"""

import re
import sys
import os
import json
import logging
import requests
import spacy

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OLLAMA_BASE_URL, LLM_MODEL

logger = logging.getLogger(__name__)

# ── spaCy — load once at module level ─────────────────────────────────────────
try:
    _nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.error("spaCy model not found. Run: python -m spacy download en_core_web_sm")
    _nlp = None

# ── Experience regex patterns ─────────────────────────────────────────────────
_EXP_PATTERNS = [
    r"(\d+)\+?\s*years?\s+of\s+experience",
    r"(\d+)\+?\s*years?\s+experience",
    r"experience\s+of\s+(\d+)\+?\s*years?",
    r"(\d+)\+?\s*yrs?\s+of\s+experience",
    r"(\d+)\+?\s*yrs?\s+experience",
]


# ─────────────────────────────────────────────────────────────────────────────
# INDIVIDUAL EXTRACTORS
# ─────────────────────────────────────────────────────────────────────────────

def extract_name(text: str) -> str:
    """
    Extract candidate name using spaCy NER.
    Checks the first 600 characters where the name is almost always found.
    Returns 'Unknown' if nothing is detected.
    """
    if not _nlp:
        return "Unknown"
    doc = _nlp(text[:600])
    for ent in doc.ents:
        if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
            return ent.text.strip()
    # fallback: any PERSON entity even single name
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()
    return "Unknown"


def extract_location(text: str) -> str:
    """
    Extract candidate location using spaCy GPE (geo-political entity).
    Checks the first 1500 characters.
    Returns 'Unknown' if nothing is detected.
    """
    if not _nlp:
        return "Unknown"
    doc = _nlp(text[:1500])
    for ent in doc.ents:
        if ent.label_ in ("GPE", "LOC"):
            return ent.text.strip()
    return "Unknown"


def extract_experience_years(text: str) -> int:
    """
    Extract total years of experience using regex.
    Returns the largest number found (most likely total experience).
    Returns 0 if no pattern matches.
    """
    found = []
    text_lower = text.lower()
    for pattern in _EXP_PATTERNS:
        for match in re.finditer(pattern, text_lower):
            found.append(int(match.group(1)))
    return max(found) if found else 0


def extract_skills_via_llm(text: str) -> list[str]:
    """
    Use the Ollama LLM to extract all technical skills from resume text.

    No hardcoded skills list — the LLM reads the resume and identifies
    every technical skill, tool, framework, language, and platform mentioned.

    Falls back to an empty list if the LLM call fails, so ingestion
    never breaks even if Ollama is temporarily unavailable.
    """
    # Use first 3000 chars — enough to capture skills section
    # without exceeding context limits or adding unnecessary cost
    excerpt = text[:3000].strip()

    prompt = f"""You are a resume parser. Extract ALL technical skills from the resume text below.

Include: programming languages, frameworks, libraries, tools, platforms, databases,
cloud services, methodologies, and any other technical competencies mentioned.

Resume text:
\"\"\"
{excerpt}
\"\"\"

Rules:
- Respond ONLY with a valid JSON array of strings.
- Each item must be a single skill or technology name.
- Normalise capitalisation: use "Python" not "python", "AWS" not "aws".
- Do NOT include soft skills (communication, leadership, teamwork etc.).
- Do NOT include job titles or company names.
- Do NOT add any explanation, markdown, or text outside the JSON array.

Example output format:
["Python", "FastAPI", "PostgreSQL", "Docker", "AWS", "React"]
"""

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={"model": LLM_MODEL, "prompt": prompt, "stream": False},
            timeout=90
        )
        response.raise_for_status()
        raw = response.json().get("response", "").strip()

        # Strip markdown fences if the LLM added them
        clean = raw.strip()
        if clean.startswith("```"):
            clean = re.sub(r"^```[a-z]*\n?", "", clean)
            clean = re.sub(r"```$", "", clean).strip()

        skills = json.loads(clean)

        if not isinstance(skills, list):
            raise ValueError("LLM response is not a JSON array")

        # Sanitise: keep only strings, strip whitespace, deduplicate
        skills = list({s.strip() for s in skills if isinstance(s, str) and s.strip()})
        logger.info(f"LLM extracted {len(skills)} skills")
        return skills

    except requests.exceptions.ConnectionError:
        logger.error("Ollama not reachable during skill extraction. Returning empty skills.")
        return []
    except (json.JSONDecodeError, ValueError) as e:
        logger.warning(f"Skill extraction LLM parse failed: {e}. Raw: {raw[:200]}")
        return []
    except Exception as e:
        logger.error(f"Skill extraction failed unexpectedly: {e}")
        return []


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def extract_metadata(text: str) -> dict:
    """
    Run all extractors on resume text and return a metadata dict
    ready to be stored in ChromaDB.

    Returns:
        {
            "candidate_name":   str,
            "skills":           str   (comma-separated, for ChromaDB string field),
            "experience_years": int,
            "location":         str,
            "skills_count":     int,
        }
    """
    skills = extract_skills_via_llm(text)

    metadata = {
        "candidate_name":   extract_name(text),
        "skills":           ", ".join(skills),   # ChromaDB requires string, not list
        "experience_years": extract_experience_years(text),
        "location":         extract_location(text),
        "skills_count":     len(skills),
    }

    logger.debug(f"Extracted metadata: {metadata}")
    return metadata
