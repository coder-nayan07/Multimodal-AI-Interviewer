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

    topic: str = Field(
        description=(
            "Definition:\n"
            "A single interview topic.\n\n"

            "Requirements:\n"
            "- Must originate from the Resume, Job Description or both.\n"
            "- Must be specific.\n"
            "- Must represent one interview discussion area.\n\n"

            "Do NOT:\n"
            "- Combine unrelated technologies.\n"
            "- Invent new topics."
        )
    )

    objective: str = Field(
        description=(
            "Definition:\n"
            "Describe exactly what the interviewer wants to verify "
            "while discussing this topic.\n\n"

            "Example:\n"
            "Evaluate the candidate's understanding of architectural "
            "decisions made during the project."
        )
    )

    source: Literal["resume", "job_description"] = Field(
        description="""
        Source of this interview topic.

        Output EXACTLY one of:
        - resume
        - job_description
        - both
        """
    )

    evidence: list[str] = Field(
        description=(
            "Concrete resume or JD evidence supporting "
            "this topic."
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
