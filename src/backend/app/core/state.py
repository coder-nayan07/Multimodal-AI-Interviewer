from typing import List, Optional, Literal, TypedDict
from pydantic import BaseModel, Field

# --- Shared Data Models ---

class Question(BaseModel):
    id: str = Field(..., description="Unique ID for frontend tracking")
    category: Literal["technical", "behavioral", "system_design"]
    topic: str
    content: str
    difficulty: int
    expected_keywords: List[str]

class CandidateProfile(BaseModel):
    name: str
    years_of_experience: float
    primary_tech_stack: List[str]
    weakness_areas: List[str]

class InterviewPlan(BaseModel):
    candidate: CandidateProfile
    question_bank: List[Question]

# --- The Graph State (Memory) ---

class InterviewState(TypedDict):
    """
    The Single Source of Truth for the interview session.
    """
    resume_text: str
    candidate_profile: Optional[CandidateProfile]
    
    # The Plan
    question_bank: List[Question]
    current_question_index: int
    
    # Conversation History (Chat Log)
    messages: List[dict] 
    
    # Real-time Feedback
    current_answer_feedback: Optional[str]
    interview_score: float