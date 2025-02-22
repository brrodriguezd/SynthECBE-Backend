from typing import List
from PyPDF2 import PdfReader
from pathlib import Path
from instances import lm
import numpy as np
from io import BytesIO

def process_pdf(pdf_content: str | Path) -> List[str]:
    """Extract and chunk text from PDF."""

    if isinstance(pdf_content, bytes):
        pdf_file = BytesIO(pdf_content)
    elif isinstance(pdf_content, (str, Path)):
        pdf_file = Path(pdf_content) if not isinstance(pdf_content, Path) else pdf_content
    else:
        raise ValueError("pdf_content must be a file path (str/Path) or bytes")
    reader = PdfReader(pdf_file)
    chunks = []
    for page in reader.pages:
        raw_text = page.extract_text()
        if raw_text:
            paragraphs = [para.strip() for para in raw_text.split('\n\n') if para.strip()]
            # preprocces each paragraph
            chunks.extend(paragraphs)
    return chunks

def compute_embedding(text: str) -> np.ndarray:
    """Compute embedding for a text chunk."""
    tensor = lm.model.encode(text)
    return tensor.numpy()
