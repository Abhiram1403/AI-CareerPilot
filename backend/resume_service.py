from pathlib import Path

from docx import Document
from fastapi import UploadFile
from pypdf import PdfReader

UPLOAD_DIR = Path("database/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


async def save_resume(file: UploadFile) -> Path:
    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Only PDF and DOCX resumes are supported")

    safe_filename = Path(file.filename or "resume").name
    file_path = UPLOAD_DIR / safe_filename

    content = await file.read()
    file_path.write_bytes(content)

    return file_path


def extract_text_from_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))

    text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text).strip()


def extract_text_from_docx(file_path: Path) -> str:
    document = Document(str(file_path))

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)


def extract_resume_text(file_path: Path) -> str:
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".docx":
        return extract_text_from_docx(file_path)

    raise ValueError("Unsupported resume format")