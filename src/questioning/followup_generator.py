from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_client import LLMClient
from src.llm.prompts import FOLLOW_UP_PROMPT

from src.models.schemas import (
    FollowUpQuestion,
    InterviewTopic,
)


class FollowUpGenerator:

    def __init__(self):

        self.llm = LLMClient().get_llm()

        self.structured_llm = self.llm.with_structured_output(
            FollowUpQuestion
        )

        self.prompt = ChatPromptTemplate.from_template(
            FOLLOW_UP_PROMPT
        )

    def generate(
        self,
        topic: InterviewTopic,
        conversation: str,
    ) -> FollowUpQuestion:

        chain = self.prompt | self.structured_llm

        return chain.invoke(
            {
                "topic": topic.model_dump_json(indent=2),
                "conversation": conversation,
            }
        )