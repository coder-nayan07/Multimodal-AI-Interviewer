from langgraph.graph import StateGraph, END, START
from src.backend.app.core.state import InterviewState
from src.backend.app.services.resume_parser import ResumeArchitect

# --- NODES (The Actions) ---

async def init_interview(state: InterviewState):
    """Node 1: Parse Resume & Generate Questions"""
    print("--- NODE: Init Interview ---")
    
    # We use the path stored in the state, or default to sample
    pdf_path = state.get("resume_text", "sample_resume.pdf") 
    
    architect = ResumeArchitect()
    plan = await architect.process_resume(pdf_path) 
    
    # Initialize the conversation with a Greeting
    greeting = f"Hello {plan.candidate.name}. I've reviewed your profile. I see you have experience with {', '.join(plan.candidate.primary_tech_stack[:2])}. Let's begin."
    
    return {
        "candidate_profile": plan.candidate,
        "question_bank": plan.question_bank,
        "current_question_index": 0,
        "messages": [{"role": "ai", "content": greeting}]
    }

def ask_question(state: InterviewState):
    """Node 2: Ask the current question"""
    print("--- NODE: Ask Question ---")
    idx = state["current_question_index"]
    questions = state["question_bank"]
    
    # Check if we are done
    if idx >= len(questions):
        return {"messages": [{"role": "ai", "content": "Thank you. The interview is complete."}]}
        
    current_q = questions[idx]
    message = f"Question {idx+1} ({current_q.topic}): {current_q.content}"
    
    return {"messages": [{"role": "ai", "content": message}]}

def process_answer(state: InterviewState):
    """Node 3: Receive User Answer & Decide Next Step"""
    print("--- NODE: Process Answer ---")
    
    # In the next phase, we will add LLM Grading here.
    # For now, we simulate a "Perfect Answer" and move forward.
    
    next_idx = state["current_question_index"] + 1
    return {"current_question_index": next_idx}

# --- EDGES (The Router) ---

def route_next(state: InterviewState):
    """Logic: Are we out of questions?"""
    if state["current_question_index"] >= len(state["question_bank"]):
        return "end"
    return "ask_question"

# --- GRAPH BUILDER ---

workflow = StateGraph(InterviewState)

# 1. Add Nodes
workflow.add_node("init_interview", init_interview)
workflow.add_node("ask_question", ask_question)
workflow.add_node("process_answer", process_answer)

# 2. Add Edges
workflow.add_edge(START, "init_interview")
workflow.add_edge("init_interview", "ask_question")
# Critical: After processing an answer, we loop back to ask the next question
workflow.add_edge("process_answer", "ask_question") 

# 3. Conditional Exit
workflow.add_conditional_edges(
    "ask_question",
    route_next,
    {
        "ask_question": END, # Wait for user input (in a real app)
        "end": END
    }
)

app = workflow.compile()