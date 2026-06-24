import re
from pathlib import Path
from typing import Dict
import sys
import os
import fitz

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.models.schemas import ResumeDocument


class ResumeParser:
    """
    Parses a PDF resume into a structured ResumeDocument.
    """

    SECTION_HEADERS = {
        "education": [
            "education",
            "academic background",
            "academic qualifications",
        ],
        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment history",
        ],
        "projects": [
            "projects",
            "project experience",
            "academic projects",
        ],
        "skills": [
            "skills",
            "technical skills",
            "core competencies",
            "technologies",
        ],
        "publications": [
            "publications",
            "research publications",
            "papers",
        ],
        "achievements": [
            "achievements",
            "awards",
            "honors",
            "accomplishments",
        ],
        "certifications": [
            "certifications",
            "certificates",
        ],
        "leadership": [
            "leadership",
            "positions of responsibility",
            "responsibilities",
        ],
    }

    def parse(self, pdf_path: str) -> ResumeDocument:
        """
        Main entry point.
        """

        raw_text = self._extract_text(pdf_path)

        cleaned_text = self._clean_text(raw_text)

        sections = self._extract_sections(cleaned_text)

        return ResumeDocument(
            file_name=Path(pdf_path).name,
            raw_text=raw_text,
            cleaned_text=cleaned_text,
            sections=sections,
        )

    def _extract_text(self, pdf_path: str) -> str:
        """
        Extract text from PDF using PyMuPDF.
        """

        document = fitz.open(pdf_path)

        pages = []

        for page in document:
            pages.append(page.get_text())

        document.close()

        return "\n".join(pages)

    def _clean_text(self, text: str) -> str:

        text = re.sub(r"[^\x00-\x7F]+", " ", text)

        text = text.replace("\t", " ")

        text = re.sub(r"[ ]+", " ", text)

        text = re.sub(r"\n{3,}", "\n\n", text)

        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line]

        return "\n".join(lines)

    def _extract_sections(self, text: str) -> Dict[str, str]:
        """
        Heuristic section extraction.
        """

        lines = text.split("\n")

        sections = {}

        current_section = "general"

        sections[current_section] = []

        for line in lines:
            normalized_line = line.strip().lower()

            detected_section = self._detect_section(normalized_line)

            if detected_section:
                current_section = detected_section

                if current_section not in sections:
                    sections[current_section] = []

                continue

            sections[current_section].append(line)

        return {
            section: "\n".join(content).strip()
            for section, content in sections.items()
            if content
        }

    def _detect_section(self, line: str) -> str | None:
        """
        Match a line against known resume section headers.
        """

        line = line.strip().lower()

        for section_name, aliases in self.SECTION_HEADERS.items():
            for alias in aliases:
                if line == alias:
                    return section_name

        return None