from typing import Literal

from src.models.schemas import (
    InterviewPlan,
    InterviewQuestion,
    InterviewSession,
    InterviewTopic,
    InterviewTurn,
    AnswerEvaluation,
)


class InterviewEngine:
    """
    Controls the interview flow.

    This class is purely deterministic and contains
    no LLM calls.
    """

    # ======================================================
    # Session Management
    # ======================================================

    def start(
        self,
        interview_plan: InterviewPlan,
    ) -> InterviewSession:
        """
        Creates a fresh interview session.
        """

        if not interview_plan.topics:
            raise ValueError(
                "Interview plan contains no topics."
            )

        return InterviewSession(
            interview_plan=interview_plan,
        )

    def is_finished(
        self,
        session: InterviewSession,
    ) -> bool:
        """
        Returns True if the interview is complete.
        """

        return session.completed

    # ======================================================
    # Topic Management
    # ======================================================

    def current_topic(
        self,
        session: InterviewSession,
    ) -> InterviewTopic:
        """
        Returns the current interview topic.
        """

        if session.completed:
            raise RuntimeError(
                "Interview has already completed."
            )

        return session.interview_plan.topics[
            session.current_topic_index
        ]

    def advance(
        self,
        session: InterviewSession,
    ) -> None:
        """
        Advances the interview to the next topic.
        """

        if session.completed:
            return

        session.current_topic_index += 1

        if (
            session.current_topic_index
            >= len(session.interview_plan.topics)
        ):
            session.completed = True

    # ======================================================
    # Turn Management
    # ======================================================

    def add_turn(
        self,
        session: InterviewSession,
        question: InterviewQuestion,
        turn_type: Literal[
            "initial",
            "follow_up",
        ] = "initial",
    ) -> InterviewTurn:
        """
        Creates a new interview turn.
        """

        turn = InterviewTurn(
            topic=self.current_topic(session),
            question=question,
            turn_type=turn_type,
        )

        session.turns.append(turn)

        return turn

    def current_turn(
        self,
        session: InterviewSession,
    ) -> InterviewTurn | None:
        """
        Returns the latest interview turn.
        """

        if not session.turns:
            return None

        return session.turns[-1]

    def record_answer(
        self,
        session: InterviewSession,
        answer: str,
    ) -> None:
        """
        Stores the candidate's answer.
        """

        turn = self.current_turn(session)

        if turn is None:
            raise RuntimeError(
                "Cannot record an answer before asking a question."
            )

        turn.candidate_answer = answer

    def record_evaluation(
        self,
        session: InterviewSession,
        evaluation: AnswerEvaluation,
    ) -> None:
        """
        Stores the evaluation for the current turn.
        """

        turn = self.current_turn(session)

        if turn is None:
            raise RuntimeError(
                "Cannot evaluate before asking a question."
            )

        turn.evaluation = evaluation

    # ======================================================
    # Conversation History
    # ======================================================

    def topic_history(
        self,
        session: InterviewSession,
    ) -> str:
        """
        Returns the conversation history for the
        current interview topic.
        """

        topic = self.current_topic(session)

        history = []

        for turn in session.turns:

            if turn.topic.topic != topic.topic:
                continue

            history.append(
                f"Question:\n{turn.question.question}"
            )

            if turn.candidate_answer:

                history.append(
                    f"Candidate:\n{turn.candidate_answer}"
                )

        return "\n\n".join(history)