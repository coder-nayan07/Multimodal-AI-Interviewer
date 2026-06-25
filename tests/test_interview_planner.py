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

planner = InterviewPlanner()

plan = planner.generate(
    resume,
    jd,
    planning_context,
)

print("=" * 100)
print("INTERVIEW PLAN")
print("=" * 100)

for idx, topic in enumerate(plan.topics, start=1):

    print(f"\nTopic {idx}")

    print(f"Title      : {topic.topic}")
    print(f"Source     : {topic.source}")
    print(f"Objective  : {topic.objective}")

print("\nStrategy")
print(plan.interview_strategy)

print("\nTotal Topics:", len(plan.topics))
