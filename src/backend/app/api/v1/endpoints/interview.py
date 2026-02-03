from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.backend.app.core.graph import app as interview_graph
import json

router = APIRouter()

@router.websocket("/ws/interview/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    print(f"--- Client {client_id} Connected ---")
    
    # Initialize State
    current_state = {
        "messages": [], 
        "current_question_index": 0, 
        "evaluations": [],
        "question_bank": [] # Ensure this exists
    }
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # --- DEBUG LOG ---
            print(f"\nSTART TURN | Current Index: {current_state.get('current_question_index')}")

            # CASE 1: START INTERVIEW
            if message["type"] == "init":
                print(f"Initializing with resume: {message['payload']}")
                current_state["resume_text"] = message["payload"]
                
                async for event in interview_graph.astream(current_state):
                    for node, values in event.items():
                        current_state.update(values)
                        
                        if "messages" in values:
                            ai_msg = values["messages"][-1]["content"]
                            await websocket.send_json({
                                "type": "ai_response",
                                "payload": ai_msg
                            })

            # CASE 2: USER ANSWERS
            elif message["type"] == "answer":
                print(f"Received Answer: {message['payload'][:30]}...")
                
                # Append user answer to history
                current_state["messages"].append({"role": "user", "content": message["payload"]})
                
                # Run Graph
                async for event in interview_graph.astream(current_state):
                     for node, values in event.items():
                        
                        # Update State IMMEDIATELY
                        current_state.update(values)
                        
                        # Debug: Check if index updated
                        if "current_question_index" in values:
                             print(f"State Updated: Index -> {values['current_question_index']}")

                        # Send Feedback (Score)
                        if "evaluations" in values:
                            latest_eval = values["evaluations"][-1]
                            await websocket.send_json({
                                "type": "feedback",
                                "payload": {
                                    "score": latest_eval.score,
                                    "feedback": latest_eval.feedback
                                }
                            })
                        
                        # Send Next Question
                        if "messages" in values:
                            last_msg = values["messages"][-1]
                            if last_msg["role"] == "ai":
                                await websocket.send_json({
                                    "type": "ai_response",
                                    "payload": last_msg["content"]
                                })

            # --- DEBUG LOG ---
            print(f" END TURN | New Index: {current_state.get('current_question_index')}")

    except WebSocketDisconnect:
        print(f"--- Client {client_id} Disconnected ---")