from src.models.schemas import (
    InterviewPlan,
    InterviewQuestion,
    InterviewSession,
    InterviewTopic,
    InterviewTurn,
)


class InterviewEngine:
    """
    Controls the interview flow.

    This class is purely deterministic and contains
    no LLM calls.
    """

    def topic_history(
        self,
        session: InterviewSession,
    ) -> str:
        """
        Returns the conversation history for the
        current interview topic.
        """

        current_topic = self.current_topic(session)

        history = []

        for turn in session.turns:

            if turn.topic.topic != current_topic.topic:
                continue

            history.append(
                f"Question:\n{turn.question.question}"
            )

            if turn.candidate_answer:

                history.append(
                    f"Candidate:\n{turn.candidate_answer}"
                )

        return "\n\n".join(history)

    def start(
        self,
        interview_plan: InterviewPlan,
    ) -> InterviewSession:
        """
        Creates a fresh interview session.
        """

        return InterviewSession(
            interview_plan=interview_plan,
        )

    def current_topic(
        self,
        session: InterviewSession,
    ) -> InterviewTopic:
        """
        Returns the current interview topic.
        """

        return session.interview_plan.topics[
            session.current_topic_index
        ]

    def add_turn(
        self,
        session: InterviewSession,
        question: InterviewQuestion,
    ) -> InterviewTurn:
        """
        Records a newly generated interview question.
        """

        turn = InterviewTurn(
            topic=self.current_topic(session),
            question=question,
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
        Stores the candidate's answer for the
        current interview turn.
        """

        turn = self.current_turn(session)

        if turn is None:
            raise RuntimeError(
                "Cannot record an answer before asking a question."
            )

        turn.candidate_answer = answer

    def advance(
        self,
        session: InterviewSession,
    ) -> None:
        """
        Advances the interview to the next topic.
        """

        session.current_topic_index += 1

        if session.current_topic_index >= len(
            session.interview_plan.topics
        ):
            session.completed = True

    def is_finished(
        self,
        session: InterviewSession,
    ) -> bool:
        """
        Returns True if the interview is complete.
        """

        return session.completed