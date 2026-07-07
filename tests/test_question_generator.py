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


resume = ResumeParser().parse(
    "data/NAYAN_.pdf"
)

jd = JobDescriptionParser().parse(
    "data/JD.txt"
)

planning_context = CandidateProfiler().generate(
    resume,
    jd,
)

interview_plan = InterviewPlanner().generate(
    resume,
    jd,
    planning_context,
)

generator = QuestionGenerator()

topic = interview_plan.topics[0]

question = generator.generate(
    topic,
)

print("=" * 80)
print("CURRENT TOPIC")
print("=" * 80)
print(topic.model_dump())

print()

print("=" * 80)
print("GENERATED QUESTION")
print("=" * 80)
print(question.model_dump())