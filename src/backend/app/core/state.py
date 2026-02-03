from typing import List, Optional, Literal, TypedDict
from pydantic import BaseModel, Field

# --- 1. Shared Data Models ---

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

# --- NEW: Evaluation Model (The missing piece) ---
class AnswerEvaluation(BaseModel):
    score: int = Field(..., description="Score between 0-10 based on accuracy and depth")
    feedback: str = Field(..., description="Short feedback for the candidate (e.g. 'Good mention of mutex locks, but missed semaphores')")
    is_relevant: bool = Field(..., description="True if the answer actually addresses the question")

# --- 2. The Graph State (Memory) ---

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
    
    # --- NEW: Track Scores ---
    # This stores the history of every grade given by the LLM
    evaluations: List[AnswerEvaluation] 
    
    # Optional legacy fields (can keep or remove)
    current_answer_feedback: Optional[str]
    interview_score: float