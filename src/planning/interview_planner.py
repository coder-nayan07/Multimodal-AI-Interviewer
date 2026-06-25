from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_client import LLMClient
from src.llm.prompts import INTERVIEW_PLANNING_PROMPT
from src.models.schemas import (
    CandidateProfile,
    InterviewPlan,
)

class InterviewPlanner:

    def generate(
        self,
        profile: CandidateProfile
    ) -> InterviewPlan:

        return InterviewPlan(
            target_topics=profile.suggested_interview_topics[:5],

            focus_areas=profile.strengths[:3],

            probing_areas=profile.missing_skills[:3],

            question_constraints=[
                "Only ask questions related to resume, JD, or interview plan",
                "Prefer project-specific questions",
                "Probe missing skills from JD",
                "Avoid unrelated technologies",
            ],

            target_question_count=10,

            estimated_duration_minutes=25,

            interview_strategy=(
                "Start with projects, "
                "move to strengths, "
                "then probe missing skills."
            ),
        )