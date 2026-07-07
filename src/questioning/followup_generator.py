from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_client import LLMClient
from src.llm.prompts import FOLLOW_UP_PROMPT

from src.models.schemas import (
    InterviewQuestion,
    InterviewTopic,
)


class FollowUpGenerator:
    """
    Generates a follow-up interview question based on the
    previous conversation and the evaluator's feedback.
    """

    def __init__(self):

        llm = LLMClient().get_llm()

        self.structured_llm = llm.with_structured_output(
            InterviewQuestion
        )

        self.prompt = ChatPromptTemplate.from_template(
            FOLLOW_UP_PROMPT
        )

    def generate(
        self,
        topic: InterviewTopic,
        conversation: str,
        follow_up_focus: str,
    ) -> InterviewQuestion:

        chain = self.prompt | self.structured_llm

        return chain.invoke(
            {
                "topic": topic.model_dump_json(indent=2),
                "conversation": conversation,
                "follow_up_focus": follow_up_focus,
            }
        )