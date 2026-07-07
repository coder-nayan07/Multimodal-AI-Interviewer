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


# -------------------------------------------------------
# Parse Resume + JD
# -------------------------------------------------------

resume = ResumeParser().parse(
    "data/NAYAN_.pdf"
)

jd = JobDescriptionParser().parse(
    "data/JD.txt"
)

# -------------------------------------------------------
# Planning Context
# -------------------------------------------------------

planning_context = CandidateProfiler().generate(
    resume,
    jd,
)

# -------------------------------------------------------
# Interview Plan
# -------------------------------------------------------

planner = InterviewPlanner()

plan = planner.generate(
    resume,
    jd,
    planning_context,
)

# -------------------------------------------------------
# Interview Engine
# -------------------------------------------------------

engine = InterviewEngine()

session = engine.start(plan)

print("=" * 80)
print("INTERVIEW STARTED")
print("=" * 80)

print("Finished :", engine.is_finished(session))
print()

# -------------------------------------------------------
# Current Topic
# -------------------------------------------------------

topic = engine.current_topic(session)

print("=" * 80)
print("CURRENT TOPIC")
print("=" * 80)

print(topic.model_dump())
print()

# -------------------------------------------------------
# Generate Question
# -------------------------------------------------------

generator = QuestionGenerator()

question = generator.generate(
    topic,
)

print("=" * 80)
print("QUESTION")
print("=" * 80)

print(question.model_dump())
print()

# -------------------------------------------------------
# Add Turn
# -------------------------------------------------------

turn = engine.add_turn(
    session,
    question,
)

print("=" * 80)
print("TURN CREATED")
print("=" * 80)

print(turn.model_dump())
print()

# -------------------------------------------------------
# Candidate Answer
# -------------------------------------------------------

engine.record_answer(
    session,
    """
    I selected a hybrid edge-cloud architecture because
    inference latency was critical.

    Running everything remotely increased latency,
    while running everything locally required too much
    GPU memory.

    The hybrid architecture allowed me to balance
    responsiveness and computational efficiency.
    """
)

print("=" * 80)
print("UPDATED TURN")
print("=" * 80)

print(engine.current_turn(session).model_dump())
print()

# -------------------------------------------------------
# Next Topic
# -------------------------------------------------------

engine.advance(session)

print("=" * 80)
print("NEXT TOPIC")
print("=" * 80)

print(engine.current_topic(session).topic)
print()

print("=" * 80)
print("SESSION SUMMARY")
print("=" * 80)

print(f"Topics Completed : {session.current_topic_index}")
print(f"Total Turns      : {len(session.turns)}")
print(f"Interview Done   : {engine.is_finished(session)}")