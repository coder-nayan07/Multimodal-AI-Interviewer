from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_client import LLMClient
from src.llm.prompts import PROFILE_GENERATION_PROMPT
from src.models.schemas import (
    CandidateProfile,
    ResumeDocument,
    JobDescriptionDocument,
)



class CandidateProfiler:

    def __init__(self):
        self.llm = LLMClient().get_llm()

        self.structured_llm = self.llm.with_structured_output(
            CandidateProfile
        )

        self.prompt = ChatPromptTemplate.from_template(
            PROFILE_GENERATION_PROMPT
        )

    def generate(
            self,
            resume: ResumeDocument,
            jd: JobDescriptionDocument,
        ) -> CandidateProfile:

        chain = self.prompt | self.structured_llm
        resume_context = resume.to_llm_context()
        profile = chain.invoke(
            {
                "resume_text": resume_context,
                "jd_text": jd.cleaned_text,
            }
        )

        return profile