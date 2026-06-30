from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_client import LLMClient
from src.llm.prompts import INTERVIEW_REPORT_PROMPT

from src.models.schemas import (
    InterviewSession,
    InterviewReport,
)


class InterviewReportGenerator:

    def __init__(self):

        self.llm = LLMClient().get_llm()

        self.structured_llm = self.llm.with_structured_output(
            InterviewReport
        )

        self.prompt = ChatPromptTemplate.from_template(
            INTERVIEW_REPORT_PROMPT
        )

    def generate(
        self,
        session: InterviewSession,
    ) -> InterviewReport:

        chain = self.prompt | self.structured_llm

        report = chain.invoke(
            {
                "session": session.model_dump_json(
                    indent=2
                )
            }
        )

        return report