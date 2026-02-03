from typing import List, Optional, Literal, TypedDict, Union
from pydantic import BaseModel, Field, field_validator

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

# --- NEW: Evaluation Model (Robust Fix) ---
class AnswerEvaluation(BaseModel):
    score: Union[int, str] = Field(..., description="Score between 0-10")
    feedback: str = Field(..., description="Short feedback for the candidate")
    is_relevant: Union[bool, str] = Field(..., description="True if the answer actually addresses the question")

    @field_validator('score')
    @classmethod
    def convert_score(cls, v):
        if isinstance(v, str):
            # Handle cases where LLM outputs "8/10" or "Score: 8"
            clean_v = ''.join(filter(str.isdigit, v))
            return int(clean_v) if clean_v else 0
        return v

    @field_validator('is_relevant')
    @classmethod
    def convert_bool(cls, v):
        if isinstance(v, str):
            return v.lower() == 'true'
        return v

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
    
    # Conversation History
    messages: List[dict] 
    
    # Track Scores
    evaluations: List[AnswerEvaluation] 
    
    # Optional legacy fields
    current_answer_feedback: Optional[str]
    interview_score: float