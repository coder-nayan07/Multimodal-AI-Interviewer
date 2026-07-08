from src.models.schemas import (
    InterviewPlan,
    InterviewTopic,
    PlanningContext,
    ResumeDocument,
    JobDescriptionDocument,
)


class InterviewPlanner:
    """
    Converts a PlanningContext into an ordered InterviewPlan.

    This class contains no LLM calls and no business
    intelligence beyond deterministic ordering.
    """

    MAX_RESUME_TOPICS = 4
    MAX_JD_TOPICS = 2

    def generate(
        self,
        resume: ResumeDocument,
        jd: JobDescriptionDocument,
        planning_context: PlanningContext,
    ) -> InterviewPlan:

        topics: list[InterviewTopic] = []

        visited: set[str] = set()

        # ==================================================
        # Resume Highlights (Highest Priority)
        # ==================================================

        resume_count = 0

        for highlight in planning_context.resume_highlights:

            if resume_count >= self.MAX_RESUME_TOPICS:
                break

            key = highlight.lower()

            if key in visited:
                continue

            topics.append(
                InterviewTopic(
                    topic=highlight,
                    source="resume",
                    objective=(
                        f"Discuss the candidate's experience related to "
                        f"'{highlight}' and understand the technical "
                        "decisions, challenges, and outcomes."
                    ),
                    supporting_context=resume.find_relevant_context(
                        highlight
                    ),
                )
            )

            visited.add(key)
            resume_count += 1

        # ==================================================
        # Job Description Requirements (Second Priority)
        # ==================================================

        jd_count = 0

        for requirement in planning_context.requirements_to_verify:

            if jd_count >= self.MAX_JD_TOPICS:
                break

            key = requirement.lower()

            if key in visited:
                continue

            topics.append(
                InterviewTopic(
                    topic=requirement,
                    source="job_description",
                    objective=(
                        f"Verify the candidate's understanding and practical "
                        f"experience with '{requirement}'."
                    ),
                    supporting_context=(
                        "This topic originates from the Job Description.\n"
                        f"Requirement: {requirement}"
                    ),
                )
            )

            visited.add(key)
            jd_count += 1

        # ==================================================
        # Remaining JD Priorities (Only if slots remain)
        # ==================================================

        if jd_count < self.MAX_JD_TOPICS:

            for item in planning_context.jd_priorities:

                if jd_count >= self.MAX_JD_TOPICS:
                    break

                key = item.lower()

                if key in visited:
                    continue

                topics.append(
                    InterviewTopic(
                        topic=item,
                        source="job_description",
                        objective=(
                            f"Assess the candidate's familiarity with '{item}' "
                            "if time permits."
                        ),
                        supporting_context=(
                            "This topic originates from the Job Description.\n"
                            f"Requirement: {item}"
                        ),
                    )
                )

                visited.add(key)
                jd_count += 1

        return InterviewPlan(
            topics=topics,
            interview_strategy=(
                "Begin with the candidate's strongest resume projects and "
                "technical achievements. Use follow-up questions to probe "
                "implementation details, design decisions, and trade-offs. "
                "Conclude by verifying the most important job-description "
                "requirements that were not explicitly demonstrated in the resume."
            ),
        )