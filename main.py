from pathlib import Path

from src.parsers.resume_parser import ResumeParser
from src.parsers.jd_parser import JobDescriptionParser

from src.profiling.candidate_profiler import CandidateProfiler
from src.planning.interview_planner import InterviewPlanner

from src.questioning.question_generator import QuestionGenerator
from src.questioning.followup_generator import FollowUpGenerator

from src.evaluation.answer_evaluator import AnswerEvaluator
from src.reporting.report_generator import InterviewReportGenerator

from src.interview.interview_engine import InterviewEngine


# ==========================================================
# Configuration
# ==========================================================

RESUME_PATH = Path("data/NAYAN_.pdf")
JD_PATH = Path("data/JD.txt")


# ==========================================================
# Build Interview
# ==========================================================

def build_interview():

    print("=" * 80)
    print("BUILDING INTERVIEW")
    print("=" * 80)

    resume = ResumeParser().parse(RESUME_PATH)

    jd = JobDescriptionParser().parse(JD_PATH)

    planning_context = CandidateProfiler().generate(
        resume,
        jd,
    )

    interview_plan = InterviewPlanner().generate(
        resume,
        jd,
        planning_context,
    )

    session = InterviewEngine().start(
        interview_plan,
    )

    return session


# ==========================================================
# Interview Loop
# ==========================================================

def run_interview(session):

    engine = InterviewEngine()

    question_generator = QuestionGenerator()

    followup_generator = FollowUpGenerator()

    evaluator = AnswerEvaluator()

    while not engine.is_finished(session):

        topic = engine.current_topic(session)

        print()
        print("=" * 80)
        print(f"TOPIC {session.current_topic_index + 1}/{len(session.interview_plan.topics)}")
        print("=" * 80)

        print(topic.topic)
        print()

        # --------------------------------------------------
        # Initial Question
        # --------------------------------------------------

        question = question_generator.generate(
            topic,
        )

        engine.add_turn(
            session,
            question,
        )

        while True:

            current_turn = session.turns[-1]

            print()
            print("Interviewer:")
            print(current_turn.question.question)

            print()
            candidate_answer = input("Candidate: ")

            engine.record_answer(
                session,
                candidate_answer,
            )

            evaluation = evaluator.evaluate(
                current_turn.question,
                candidate_answer,
            )

            engine.record_evaluation(
                session,
                evaluation,
            )

            print()
            print("-" * 80)
            print("Evaluation")
            print("-" * 80)

            print(f"Understanding : {evaluation.demonstrated_understanding}")
            print(f"Next Action   : {evaluation.next_action}")

            if evaluation.next_action != "follow_up":
                break

            conversation = engine.topic_history(
                session,
            )

            followup = followup_generator.generate(
                topic,
                conversation,
                evaluation.follow_up_focus,
            )

            engine.add_turn(
                session,
                followup,
                turn_type="follow_up",
            )

        engine.advance(
            session,
        )

    return session


# ==========================================================
# Report
# ==========================================================

def generate_report(session):

    print()
    print("=" * 80)
    print("GENERATING FINAL REPORT")
    print("=" * 80)

    report = InterviewReportGenerator().generate(
        session,
    )

    print()

    print(report.model_dump_json(indent=2))

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    with open(
        output_dir / "interview_report.json",
        "w",
        encoding="utf-8",
    ) as f:

        f.write(
            report.model_dump_json(indent=4)
        )

    print()
    print("Report saved to outputs/interview_report.json")


# ==========================================================
# Main
# ==========================================================

def main():

    session = build_interview()

    session = run_interview(
        session,
    )

    generate_report(
        session,
    )


if __name__ == "__main__":

    main()