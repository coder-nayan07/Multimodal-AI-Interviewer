from pydantic import BaseModel
from typing import Dict


class ResumeDocument(BaseModel):
    file_name: str
    raw_text: str
    cleaned_text: str
    sections: Dict[str, str]