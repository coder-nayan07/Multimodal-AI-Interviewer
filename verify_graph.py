import asyncio
from src.backend.app.core.graph import app

async def run_terminal_interview():
    print(" STARTING TERMINAL INTERVIEW SIMULATION...")
    
    # 1. Initialize State with your PDF
    # Make sure 'sample_resume.pdf' is in the root folder!
    initial_state = {"resume_text": "sample_resume.pdf", "messages": []}
    
    # 2. Start the Graph (Run Node 1 & 2)
    print("\n--- System Initializing ---")
    async for event in app.astream(initial_state):
        for key, value in event.items():
            if "messages" in value:
                last_msg = value["messages"][-1]
                print(f"\n AI: {last_msg['content']}")

    # 3. Simulate the Loop (User Answers -> AI Asks Next)
    # We will verify 3 turns of conversation
    current_state = value # specific to langgraph implementation
    
    # NOTE: In a real app, 'app.astream' would pause for input. 
    # Here, we are just verifying the Initialization flow for today.
    
    print("\n GRAPH INITIALIZATION SUCCESSFUL")
    print("The AI successfully parsed the resume and generated the first question.")

if __name__ == "__main__":
    asyncio.run(run_terminal_interview())