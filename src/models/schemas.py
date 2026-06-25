from typing import Literal

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
    """Represents one interview topic."""


    topic: str = Field(
        description="Name of the interview topic."
    )

    source: Literal["resume", "job_description", "both"] = Field(
        description=(
            "Origin of the topic. "
            "'resume' means it comes from resume evidence, "
            "'job_description' means it comes from the JD, "
            "'both' means it is supported by both."
        )
    )

    priority: Literal["high", "medium", "low"] = Field(
        description=(
            "Importance of this topic in the interview."
        )
    )

    rationale: str = Field(
        description=(
            "Brief explanation describing why this topic should be discussed."
        )
    )

    evidence: list[str] = Field(
        description=(
            "Concrete evidence supporting this topic. "
            "Every evidence item must come directly from the Resume or Job Description."
        )
    )


class InterviewPlan(BaseModel):
    """Represents the complete interview plan."""


    topics: list[InterviewTopic] = Field(
        description=(
            "Ordered list of interview topics that should be discussed."
        )
    )

    question_constraints: list[str] = Field(
        description=(
            "Rules that the Question Generator must always follow while generating interview questions."
        )
    )

    target_question_count: int = Field(
        description=(
            "Approximate number of questions to ask during the interview."
        )
    )

    estimated_duration_minutes: int = Field(
        description=(
            "Estimated duration of the interview in minutes."
        )
    )

    interview_strategy: str = Field(
        description=(
            "Overall strategy describing how the interview should progress, "
            "including the order of topics and areas that require deeper probing."
        )
    )
