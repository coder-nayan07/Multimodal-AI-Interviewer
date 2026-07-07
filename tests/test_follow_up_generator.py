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
from src.questioning.followup_generator import FollowUpGenerator

from src.interview.interview_engine import InterviewEngine
from src.evaluation.answer_evaluator import AnswerEvaluator


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
# Initial Question
# ==========================================================

question_generator = QuestionGenerator()

question = question_generator.generate(
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
pipeline that combines geometric reasoning with DINOv2 visual
features.

The biggest challenge was obtaining robust grasp predictions
under heavy occlusion.

We experimented with multiple feature representations before
choosing DINOv2 because it produced much more stable embeddings.

The final system generalized well across previously unseen
objects while remaining computationally efficient.
"""

engine.record_answer(
    session,
    candidate_answer,
)

conversation = engine.topic_history(
    session
)


# ==========================================================
# Evaluate Candidate Answer
# ==========================================================

evaluator = AnswerEvaluator()

evaluation = evaluator.evaluate(
    question,
    candidate_answer,
)

# ==========================================================
# Follow-up Question
# ==========================================================

followup_generator = FollowUpGenerator()

followup = followup_generator.generate(
    topic,
    conversation,
    evaluation.follow_up_focus,
)

# ==========================================================
# Output
# ==========================================================

print("=" * 80)
print("CURRENT TOPIC")
print("=" * 80)

print(topic.model_dump())

print()

print("=" * 80)
print("INITIAL QUESTION")
print("=" * 80)

print(question.model_dump())

print()

print("=" * 80)
print("CANDIDATE ANSWER")
print("=" * 80)

print(candidate_answer)

print()

print("=" * 80)
print("CONVERSATION HISTORY")
print("=" * 80)

print(conversation)

print()

print("=" * 80)
print("ANSWER EVALUATION")
print("=" * 80)

print(evaluation.model_dump())

print()

print("=" * 80)
print("FOLLOW-UP QUESTION")
print("=" * 80)

print(followup.model_dump())