from pydantic import BaseModel
from typing import Dict


class ResumeDocument(BaseModel):
    file_name: str
    raw_text: str
    cleaned_text: str
    sections: dict[str, str]

    def to_llm_context(self) -> str:

        chunks = []

        for section, content in self.sections.items():

            chunks.append(
                f"{section.upper()}:\n{content}"
            )

        return "\n\n".join(chunks)



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


class InterviewPlan(BaseModel):

    target_topics: list[str]

    topic_weights: dict[str, int]

    target_question_count: int

    estimated_duration_minutes: int

    focus_areas: list[str]

    probing_areas: list[str]