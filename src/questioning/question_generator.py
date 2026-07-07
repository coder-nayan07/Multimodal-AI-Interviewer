from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_client import LLMClient
from src.llm.prompts import QUESTION_GENERATION_PROMPT

from src.models.schemas import (
    InterviewTopic,
    InterviewQuestion,
)


class QuestionGenerator:
    """
    Generates one interview question for the
    current interview topic.
    """

    def __init__(self):

        self.llm = LLMClient().get_llm()

        self.structured_llm = self.llm.with_structured_output(
            InterviewQuestion
        )

        self.prompt = ChatPromptTemplate.from_template(
            QUESTION_GENERATION_PROMPT
        )

    def generate(
        self,
        topic: InterviewTopic,
    ) -> InterviewQuestion:

        chain = self.prompt | self.structured_llm

        question = chain.invoke(
            {
                "interview_topic": topic.model_dump_json(indent=2),
            }
        )

        return question