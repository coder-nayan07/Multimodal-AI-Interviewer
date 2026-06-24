from pydantic import BaseModel
from typing import Dict


class ResumeDocument(BaseModel):
    file_name: str
    raw_text: str
    cleaned_text: str
    sections: Dict[str, str]

class JobDescriptionDocument(BaseModel):
    file_name: str
    raw_text: str
    cleaned_text: str

class CandidateProfile(BaseModel):
    matched_skills: list[str]

    missing_skills: list[str]

    strengths: list[str]

    weaknesses: list[str]

    suggested_interview_topics: list[str]

    project_discussion_points: list[str]

    overall_summary: str