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
        Returns the paragraph that best matches the interview topic.
        """

        topic_words = {
            word.lower()
            for word in re.findall(r"\w+", topic)
            if len(word) > 2
        }

        best_score = -1
        best_paragraph = ""

        for section in self.sections.values():

            paragraphs = re.split(r"\n\s*\n", section)

            for paragraph in paragraphs:

                paragraph_words = {
                    word.lower()
                    for word in re.findall(r"\w+", paragraph)
                }

                score = len(
                    topic_words & paragraph_words
                )

                if score > best_score:
                    best_score = score
                    best_paragraph = paragraph.strip()

        return best_paragraph

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
    """
    Represents a single interview question, either an initial
    question or a follow-up question.
    """

    question: str = Field(
        description="Exactly one open-ended interview question."
    )

    assessment_goal: str = Field(
        description=(
            "What this question is intended to assess."
        )
    )

    answer_checkpoints: list[str] = Field(
        description=(
            "Important concepts that a good answer should include. "
            "These are later used during answer evaluation."
        )
    )

    question_type: Literal[
        "initial",
        "follow_up",
    ] = Field(
        description=(
            "Indicates whether this is the first question "
            "for a topic or a follow-up question."
        )
    )


   
class AnswerEvaluation(BaseModel):
    """
    Evaluation of one candidate response.
    """

    answered_question: bool = Field(
        description="Whether the candidate actually answered the interview question."
    )

    demonstrated_understanding: Literal[
        "excellent",
        "good",
        "partial",
        "poor",
    ] = Field(
        description="Overall technical understanding demonstrated."
    )

    strengths: list[str] = Field(
        description="Technical strengths demonstrated in the answer."
    )

    missing_points: list[str] = Field(
        description="Important concepts expected but not sufficiently discussed."
    )

    evaluation_summary: str = Field(
        description="Short feedback explaining the evaluation."
    )

    next_action: Literal[
        "follow_up",
        "next_topic",
        "end_interview",
    ] = Field(
        description=(
            "Recommended next action for the interview engine."
        )
    )

    follow_up_focus: str = Field(
        description=(
            "If next_action is follow_up, specify exactly what should be explored."
        )
    )

    
class InterviewTurn(BaseModel):
    """
    Represents one complete interaction between the interviewer
    and the candidate.
    """

    topic: InterviewTopic

    question: InterviewQuestion

    candidate_answer: str = Field(
        default="",
        description="Candidate's answer to the interview question."
    )

    evaluation: AnswerEvaluation | None = Field(
        default=None,
        description=(
            "Evaluation of the candidate's answer. "
            "This field remains None until the answer has been evaluated."
        )
    )

    turn_type: Literal[
        "initial",
        "follow_up",
    ] = Field(
        default="initial",
        description=(
            "Indicates whether this interaction corresponds to the "
            "initial interview question or a follow-up question."
        )
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

 

class InterviewReport(BaseModel):

    candidate_summary: str = Field(
        description=(
            "Overall summary of the candidate's interview performance."
        )
    )

    technical_strengths: list[str] = Field(
        description=(
            "Technical strengths consistently demonstrated during the interview."
        )
    )

    improvement_areas: list[str] = Field(
        description=(
            "Topics where the candidate should improve."
        )
    )

    topics_discussed: list[str] = Field(
        description=(
            "Major interview topics that were covered."
        )
    )

    hiring_recommendation: Literal[
        "strong_hire",
        "hire",
        "lean_hire",
        "lean_no_hire",
        "no_hire",
    ] = Field(
        description="Overall hiring recommendation."
    )

    interviewer_notes: str = Field(
        description=(
            "Final notes summarizing the interview."
        )
    )