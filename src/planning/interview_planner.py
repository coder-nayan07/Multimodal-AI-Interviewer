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
            

    def generate(
        self,
        resume: ResumeDocument,
        jd: JobDescriptionDocument,
        planning_context: PlanningContext,
    ) -> InterviewPlan:

        topics: list[InterviewTopic] = []

        visited: set[str] = set()

        # ------------------------------------------
        # Resume Highlights (Highest Priority)
        # ------------------------------------------

        for highlight in planning_context.resume_highlights:

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
                        "decisions, challenges and outcomes."
                    ),
                    supporting_context=resume.find_relevant_context(
                        highlight
                    ),
                )
            )

            visited.add(key)

        # ------------------------------------------
        # Requirements To Verify
        # ------------------------------------------

        for requirement in planning_context.requirements_to_verify:

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
                        f"This topic originates from the Job Description.\n"
                        f"Requirement: {requirement}"
                    )
                )
            )

            visited.add(key)

        # ------------------------------------------
        # Remaining JD Priorities
        # ------------------------------------------

        for item in planning_context.jd_priorities:

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
                        f"This topic originates from the Job Description.\n"
                        f"Requirement: {requirement}"
                    )
                )
            )

            visited.add(key)

        return InterviewPlan(
            topics=topics,
            interview_strategy=(
                "Start with the candidate's strongest resume highlights, "
                "transition into job-specific verification topics, "
                "and conclude with any remaining important requirements."
            ),
        )