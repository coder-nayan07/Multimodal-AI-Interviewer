from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_client import LLMClient
from src.llm.prompts import PROFILE_GENERATION_PROMPT
from src.models.schemas import (
    PlanningContext,
    ResumeDocument,
    JobDescriptionDocument,
)

class CandidateProfiler:

    def __init__(self):
        self.llm = LLMClient().get_llm()

        self.structured_llm = (
            self.llm.with_structured_output(
                PlanningContext
            )
        )

        self.prompt = ChatPromptTemplate.from_template(
            PROFILE_GENERATION_PROMPT
        )

    def generate(
        self,
        resume: ResumeDocument,
        jd: JobDescriptionDocument,
    ) -> PlanningContext:

        chain = self.prompt | self.structured_llm

        summary = chain.invoke(
            {
                "resume_text": resume.to_llm_context(),
                "jd_text": jd.to_llm_context(),
            }
        )

        return summary