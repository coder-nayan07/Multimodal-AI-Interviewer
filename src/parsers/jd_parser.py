import re
from pathlib import Path

import pymupdf as fitz
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from src.models.schemas import JobDescriptionDocument


class JobDescriptionParser:
    """
    Parser for Job Description documents.

    Supports:
    - PDF files
    - TXT files

    Returns:
        JobDescriptionDocument
    """

    SUPPORTED_EXTENSIONS = {".pdf", ".txt"}

    def parse(self, file_path: str) -> JobDescriptionDocument:
        """
        Main parsing entry point.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {path.suffix}. "
                f"Supported types: {self.SUPPORTED_EXTENSIONS}"
            )

        raw_text = self._extract_text(path)

        cleaned_text = self._clean_text(raw_text)

        return JobDescriptionDocument(
            file_name=path.name,
            raw_text=raw_text,
            cleaned_text=cleaned_text,
        )

    def _extract_text(self, file_path: Path) -> str:
        """
        Dispatch extraction based on file extension.
        """

        extension = file_path.suffix.lower()

        if extension == ".pdf":
            return self._extract_pdf_text(file_path)

        if extension == ".txt":
            return self._extract_txt_text(file_path)

        raise ValueError(f"Unsupported extension: {extension}")

    def _extract_pdf_text(self, pdf_path: Path) -> str:
        """
        Extract text from PDF using PyMuPDF.
        """

        document = fitz.open(str(pdf_path))

        pages = []

        try:
            for page in document:
                pages.append(page.get_text())

        finally:
            document.close()

        return "\n".join(pages)

    def _extract_txt_text(self, txt_path: Path) -> str:
        """
        Extract text from TXT file.
        """

        with open(txt_path, "r", encoding="utf-8") as file:
            return file.read()

    def _clean_text(self, text: str) -> str:
        """
        Basic text normalization and cleanup.
        """

        # Remove non-ascii artifacts
        text = re.sub(r"[^\x00-\x7F]+", " ", text)

        # Replace tabs with spaces
        text = text.replace("\t", " ")

        # Collapse multiple spaces
        text = re.sub(r"[ ]+", " ", text)

        # Collapse excessive newlines
        text = re.sub(r"\n{3,}", "\n\n", text)

        lines = [line.strip() for line in text.splitlines()]

        lines = [line for line in lines if line]

        return "\n".join(lines)