from typing import Literal
import re
from pydantic import BaseModel, Field

class ResumeDocument(BaseModel):
    """Represents a parsed resume."""

    file_name: str = Field(
        description="Name of the uploaded resume file."
    )

    raw_text: str = Field(
        description="Raw text extracted directly from the resume before any cleaning."
    )

    cleaned_text: str = Field(
        description="Cleaned resume text after removing unwanted symbols, extra spaces, and formatting artifacts."
    )

    sections: dict[str, str] = Field(
        description=(
            "Dictionary containing resume sections as key-value pairs. "
            "Example: {'education': '...', 'projects': '...', 'skills': '...'}."
        )
    )

    def to_llm_context(self) -> str:
        """Formats the resume into a structured text representation for the LLM."""

        chunks = []

        for section, content in self.sections.items():
            chunks.append(
                f"{section.upper()}:\n{content}"
            )

        return "\n\n".join(chunks)

    @staticmethod
    def _normalize(text: str) -> str:
        """
        Lowercase text and remove punctuation.
        """
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def find_relevant_context(
        self,
        topic: str,
    ) -> str:
        """
        Finds the paragraph most relevant to the supplied topic using
        keyword overlap instead of exact string matching.
        """

        topic_tokens = set(
            self._normalize(topic).split()
        )

        best_match = ""
        best_score = 0

        for section_text in self.sections.values():

            paragraphs = re.split(
                r"\n\s*\n",
                section_text,
            )

            for paragraph in paragraphs:

                paragraph_tokens = set(
                    self._normalize(paragraph).split()
                )

                score = len(
                    topic_tokens.intersection(paragraph_tokens)
                )

                if score > best_score:

                    best_score = score
                    best_match = paragraph.strip()

        return best_match

class JobDescriptionDocument(BaseModel):
    """Represents a parsed Job Description."""


    file_name: str = Field(
        description="Name of the uploaded Job Description file."
    )

    raw_text: str = Field(
        description="Original text extracted from the Job Description."
    )

    cleaned_text: str = Field(
        description="Cleaned Job Description after removing formatting artifacts."
    )

    def to_llm_context(self) -> str:
        return self.cleaned_text


class PlanningContext(BaseModel):
    """
    Structured interview preparation context generated
    from the Resume and Job Description.
    """


    demonstrated_skills: list[str] = Field(
        description=(
            "Skills, technologies, tools, frameworks, programming languages, "
            "or technical domains explicitly demonstrated in the resume. "
            "Do NOT infer related skills."
        )
    )

    requirements_to_verify: list[str] = Field(
        description=(
            "Important technical requirements extracted from the Job Description "
            "that are not explicitly demonstrated in the resume. "
            "These are interview objectives, NOT candidate weaknesses."
        )
    )

    resume_highlights: list[str] = Field(
        description=(
            "Important resume items that deserve discussion during the interview. "
            "Examples include projects, internships, publications, leadership, "
            "open-source work, certifications, competitions, or significant achievements."
        )
    )

    jd_priorities: list[str] = Field(
        description=(
            "Most important technical requirements extracted from the Job Description. "
            "Ignore administrative details such as salary, benefits, location, etc."
        )
    )

class InterviewTopic(BaseModel):

    topic: str = Field(
        description="Title of the interview discussion topic."
    )

    objective: str = Field(
        description="What the interviewer wants to understand."
    )

    source: Literal[
        "resume",
        "job_description"
    ] = Field(
        description="Source of this interview topic."
    )

    supporting_context: str = Field(
        description=(
            "Relevant excerpt from the Resume or Job Description "
            "that provides enough technical context for generating "
            "high-quality interview questions."
        )
    )


class InterviewPlan(BaseModel):

    topics: list[InterviewTopic] = Field(
        description=(
            "Ordered list of interview topics that should be discussed."
        )
    )

    interview_strategy: str = Field(
        description=(
            "Overall strategy describing how the interview should progress, "
            "including the order of topics and areas that require deeper probing."
        )
    )

class InterviewQuestion(BaseModel):

    question: str = Field(
        description="Exactly one open-ended interview question."
    )

    intent: str = Field(
        description="What this question is intended to assess."
    )

    answer_checkpoints: list[str] = Field(
        description=(
            "Important concepts that a good answer should include. "
            "These will be reused by the evaluation module."
        )
    )

class InterviewTurn(BaseModel):
    """
    One complete interaction between the interviewer and candidate.
    """

    topic: InterviewTopic

    question: InterviewQuestion

    candidate_answer: str = Field(
        default="",
        description="Candidate's answer to the interview question."
    )

    
class InterviewSession(BaseModel):
    """
    Represents the complete state of an interview.
    """

    interview_plan: InterviewPlan

    current_topic_index: int = 0

    turns: list[InterviewTurn] = Field(
        default_factory=list
    )

    completed: bool = False

class FollowUpQuestion(BaseModel):

    question: str = Field(
        description="Exactly one follow-up interview question."
    )

    assessment_goal: str = Field(
        description=(
            "What this follow-up question is intended to assess."
        )
    )

    answer_checkpoints: list[str] = Field(
        description=(
            "Important concepts expected in a strong answer."
        )
    )