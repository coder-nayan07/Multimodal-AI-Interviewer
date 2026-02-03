from langgraph.graph import StateGraph, END, START
from src.backend.app.core.state import InterviewState, AnswerEvaluation
from src.backend.app.services.resume_parser import ResumeArchitect
from src.backend.app.core.config import settings
from groq import Groq
import instructor

# --- INIT CLIENTS ---
grading_client = instructor.from_groq(
    Groq(api_key=settings.GROQ_API_KEY),
    mode=instructor.Mode.TOOLS
)

# --- NODES ---

async def init_interview(state: InterviewState):
    """Node 1: Parse Resume & Generate Questions"""
    print("--- NODE: Init Interview ---")
    pdf_path = state.get("resume_text", "sample_resume.pdf") 
    
    architect = ResumeArchitect()
    plan = await architect.process_resume(pdf_path) 
    
    greeting = f"Hello {plan.candidate.name}. I've reviewed your profile. I see you have experience with {', '.join(plan.candidate.primary_tech_stack[:2])}. Let's begin."
    
    return {
        "candidate_profile": plan.candidate,
        "question_bank": plan.question_bank,
        "current_question_index": 0,
        "messages": [{"role": "ai", "content": greeting}],
        "evaluations": []
    }

def ask_question(state: InterviewState):
    """Node 2: Ask the current question"""
    print("--- NODE: Ask Question ---")
    idx = state["current_question_index"]
    questions = state["question_bank"]
    
    if idx >= len(questions):
        return {"messages": [{"role": "ai", "content": "Thank you. The interview is complete."}]}
        
    current_q = questions[idx]
    message = f"Question {idx+1} ({current_q.topic}): {current_q.content}"
    
    return {"messages": [{"role": "ai", "content": message}]}

def process_answer(state: InterviewState):
    """Node 3: Grade the answer using Llama 3"""
    print("--- NODE: Grading Answer ---")
    
    current_q = state["question_bank"][state["current_question_index"]]
    
    # Get the last message which should be the user's answer
    user_answer = state["messages"][-1]["content"]
    
    print(f"Grading Input: '{user_answer[:30]}...'")

    # Call LLM to Grade
    evaluation = grading_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a Senior Technical Interviewer. Grade the candidate's answer strictly."},
            {"role": "user", "content": f"""
            QUESTION: {current_q.content}
            EXPECTED KEYWORDS: {current_q.expected_keywords}
            
            CANDIDATE ANSWER: {user_answer}
            
            Task:
            1. Did they answer the specific question asked?
            2. specific technical accuracy?
            3. Give a score (0-10). 
            """}
        ],
        response_model=AnswerEvaluation
    )
    
    print(f"Result: Score {evaluation.score}/10. Feedback: {evaluation.feedback}")

    # Append evaluation and move index
    current_evals = state.get("evaluations", [])
    current_evals.append(evaluation)
    
    next_idx = state["current_question_index"] + 1
    
    return {
        "current_question_index": next_idx,
        "evaluations": current_evals
    }

# --- EDGES & ROUTING ---

def route_start(state: InterviewState):
    # If questions exist, we are mid-interview (process answer)
    # If not, we are starting (init)
    if state.get("question_bank") and len(state["question_bank"]) > 0:
        return "process_answer"
    return "init_interview"

def route_next(state: InterviewState):
    if state["current_question_index"] >= len(state["question_bank"]):
        return "end"
    return "ask_question"

# --- GRAPH BUILDER ---

workflow = StateGraph(InterviewState)

workflow.add_node("init_interview", init_interview)
workflow.add_node("ask_question", ask_question)
workflow.add_node("process_answer", process_answer)

workflow.add_conditional_edges(
    START,
    route_start,
    {
        "init_interview": "init_interview",
        "process_answer": "process_answer"
    }
)

workflow.add_edge("init_interview", "ask_question")
workflow.add_edge("process_answer", "ask_question")

workflow.add_conditional_edges(
    "ask_question",
    route_next,
    {
        "ask_question": END, 
        "end": END
    }
)

app = workflow.compile()