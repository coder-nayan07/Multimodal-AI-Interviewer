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

from src.evaluation.answer_evaluator import AnswerEvaluator


# ==========================================================
# Resume & JD
# ==========================================================

resume = ResumeParser().parse(
    "data/NAYAN_.pdf"
)

jd = JobDescriptionParser().parse(
    "data/JD.txt"
)

# ==========================================================
# Planning
# ==========================================================

planning_context = CandidateProfiler().generate(
    resume,
    jd,
)

plan = InterviewPlanner().generate(
    resume,
    jd,
    planning_context,
)

topic = plan.topics[0]

# ==========================================================
# Question
# ==========================================================

question = QuestionGenerator().generate(
    topic,
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

# ==========================================================
# Evaluation
# ==========================================================

evaluation = AnswerEvaluator().evaluate(
    question,
    candidate_answer,
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
print("EXPECTED CHECKPOINTS")
print("=" * 80)

for checkpoint in question.answer_checkpoints:
    print("-", checkpoint)

print()

print("=" * 80)
print("EVALUATION")
print("=" * 80)

print(evaluation.model_dump())