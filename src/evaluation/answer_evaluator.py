from langchain_core.prompts import ChatPromptTemplate

from src.llm.llm_client import LLMClient
from src.llm.prompts import ANSWER_EVALUATION_PROMPT

from src.models.schemas import (
    InterviewQuestion,
    AnswerEvaluation,
)


class AnswerEvaluator:
    """
    Evaluates one candidate response.
    """

    def __init__(self):

        self.llm = LLMClient().get_llm()

        self.structured_llm = self.llm.with_structured_output(
            AnswerEvaluation
        )

        self.prompt = ChatPromptTemplate.from_template(
            ANSWER_EVALUATION_PROMPT
        )

    def evaluate(
        self,
        question: InterviewQuestion,
        candidate_answer: str,
    ) -> AnswerEvaluation:

        chain = self.prompt | self.structured_llm

        evaluation = chain.invoke(
            {
                "question": question.question,
                "candidate_answer": candidate_answer,
                "answer_checkpoints": "\n".join(
                    question.answer_checkpoints
                ),
            }
        )

        return evaluation
    

    