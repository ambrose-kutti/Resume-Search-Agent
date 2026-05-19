import os
import fitz  # PyMuPDF
import docx
import logging

logger = logging.getLogger(__name__)


def parse_pdf(file_path: str) -> str:
    """Extract text from a PDF resume."""
    try:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        logger.error(f"Failed to parse PDF {file_path}: {e}")
        return ""


def parse_docx(file_path: str) -> str:
    """Extract text from a DOCX resume."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        logger.error(f"Failed to parse DOCX {file_path}: {e}")
        return ""


def parse_resume(file_path: str) -> str:
    """
    Auto-detect file type and extract text.
    Returns empty string if file type is unsupported.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext == ".docx":
        return parse_docx(file_path)
    else:
        logger.warning(f"Unsupported file type: {file_path}")
        return ""


def load_all_resumes(resumes_dir: str) -> list[dict]:
    """
    Walk the resumes directory and parse every PDF and DOCX file.

    Returns a list of dicts:
        {
            "file_name": "john_doe.pdf",
            "file_path": "C:/...resumes/john_doe.pdf",
            "text": "extracted resume text..."
        }
    """
    results = []

    if not os.path.exists(resumes_dir):
        logger.error(f"Resumes directory not found: {resumes_dir}")
        return results

    for file_name in os.listdir(resumes_dir):
        if not file_name.lower().endswith((".pdf", ".docx")):
            continue

        file_path = os.path.join(resumes_dir, file_name)
        logger.info(f"Parsing: {file_name}")

        text = parse_resume(file_path)

        if text:
            results.append({
                "file_name": file_name,
                "file_path": file_path,
                "text": text
            })
        else:
            logger.warning(f"Empty text extracted from: {file_name}")

    logger.info(f"Successfully parsed {len(results)} resumes.")
    return results