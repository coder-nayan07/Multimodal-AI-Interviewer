import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
        )
    )
)

from src.parsers.resume_parser import ResumeParser
from src.parsers.jd_parser import JobDescriptionParser

from src.profiling.candidate_profiler import CandidateProfiler
from src.planning.interview_planner import InterviewPlanner

from src.questioning.question_generator import QuestionGenerator
from src.interview.interview_engine import InterviewEngine

from src.evaluation.answer_evaluator import AnswerEvaluator
from src.reporting.report_generator import InterviewReportGenerator


# ==========================================================
# Parse Resume & Job Description
# ==========================================================

resume = ResumeParser().parse(
    "data/NAYAN_.pdf"
)

jd = JobDescriptionParser().parse(
    "data/JD.txt"
)

# ==========================================================
# Candidate Profiling
# ==========================================================

planning_context = CandidateProfiler().generate(
    resume,
    jd,
)

# ==========================================================
# Interview Planning
# ==========================================================

planner = InterviewPlanner()

plan = planner.generate(
    resume,
    jd,
    planning_context,
)

# ==========================================================
# Interview Engine
# ==========================================================

engine = InterviewEngine()

session = engine.start(
    plan
)

topic = engine.current_topic(
    session
)

# ==========================================================
# Generate Initial Question
# ==========================================================

question_generator = QuestionGenerator()

question = question_generator.generate(
    resume,
    jd,
    topic,
)

engine.add_turn(
    session,
    question,
)

# ==========================================================
# Simulated Candidate Answer
# ==========================================================

candidate_answer = """
For the GRIM project, we designed a multi-view grasp perception
pipeline using DINOv2 visual features.

The biggest challenge was handling severe occlusion.

We evaluated multiple feature extractors and selected DINOv2
because it produced more stable embeddings and generalized
better to unseen objects.

The final system balanced robustness with computational
efficiency.
"""

engine.record_answer(
    session,
    candidate_answer,
)

# ==========================================================
# Evaluate Answer
# ==========================================================

evaluator = AnswerEvaluator()

evaluation = evaluator.evaluate(
    question,
    candidate_answer,
)

# Save evaluation inside the interview turn

engine.current_turn(
    session
).evaluation = evaluation

# ==========================================================
# Generate Final Report
# ==========================================================

report_generator = InterviewReportGenerator()

report = report_generator.generate(
    session
)

# ==========================================================
# Output
# ==========================================================

print("=" * 80)
print("QUESTION")
print("=" * 80)
print(question.model_dump())

print()

print("=" * 80)
print("CANDIDATE ANSWER")
print("=" * 80)
print(candidate_answer)

print()

print("=" * 80)
print("ANSWER EVALUATION")
print("=" * 80)
print(evaluation.model_dump())

print()

print("=" * 80)
print("INTERVIEW REPORT")
print("=" * 80)
print(report.model_dump())