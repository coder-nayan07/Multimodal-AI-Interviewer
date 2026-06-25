import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

profile = CandidateProfiler().generate(
    resume,
    jd
)

plan = InterviewPlanner().generate(
    profile
)

print(plan.model_dump())