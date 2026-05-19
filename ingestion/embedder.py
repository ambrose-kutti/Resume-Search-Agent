import requests
import logging

logger = logging.getLogger(__name__)


def get_embedding(text: str, ollama_base_url: str, model: str) -> list[float]:
    """
    Generate a vector embedding for a given text using Ollama.
    Uses the nomic-embed-text model by default.

    Args:
        text:            The resume or query text to embed.
        ollama_base_url: Ollama server URL (default: http://localhost:11434)
        model:           Ollama embedding model name

    Returns:
        A list of floats representing the embedding vector.
        Returns an empty list on failure.
    """
    try:
        response = requests.post(
            f"{ollama_base_url}/api/embeddings",
            json={"model": model, "prompt": text},
            timeout=60
        )
        response.raise_for_status()
        embedding = response.json().get("embedding", [])
        return embedding

    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Ollama. Make sure Ollama is running: ollama serve")
        return []
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        return []


def get_embeddings_batch(
    texts: list[str],
    ollama_base_url: str,
    model: str
) -> list[list[float]]:
    """
    Generate embeddings for a list of texts.
    Processes one at a time (Ollama does not support true batching).
    Logs progress every 10 resumes.
    """
    embeddings = []
    total = len(texts)

    for i, text in enumerate(texts):
        embedding = get_embedding(text, ollama_base_url, model)
        embeddings.append(embedding)

        if (i + 1) % 10 == 0 or (i + 1) == total:
            logger.info(f"Embedded {i + 1}/{total} resumes")

    return embeddings