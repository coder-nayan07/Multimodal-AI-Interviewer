from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.backend.app.core.graph import app as interview_graph
import json

router = APIRouter()

@router.websocket("/ws/interview/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    print(f"--- Client {client_id} Connected ---")
    
    current_state = {"messages": [], "current_question_index": 0, "evaluations": []}
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # CASE 1: START INTERVIEW
            if message["type"] == "init":
                print(f"Initializing with resume: {message['payload']}")
                current_state["resume_text"] = message["payload"]
                
                async for event in interview_graph.astream(current_state):
                    for node, values in event.items():
                        if "messages" in values:
                            ai_msg = values["messages"][-1]["content"]
                            await websocket.send_json({
                                "type": "ai_response",
                                "payload": ai_msg
                            })
                            current_state.update(values)

            # CASE 2: USER ANSWERS
            elif message["type"] == "answer":
                print(f"Received Answer: {message['payload']}")
                
                # CRITICAL: Append user answer to history so Grader can see it
                current_state["messages"].append({"role": "user", "content": message["payload"]})
                
                # Run Graph (Router will send this to 'process_answer' node)
                async for event in interview_graph.astream(current_state):
                     for node, values in event.items():
                        
                        # Update state with the Grading results
                        if "evaluations" in values:
                            current_state["evaluations"] = values["evaluations"]
                            
                        if "messages" in values:
                            last_msg = values["messages"][-1]
                            # Only send AI messages to frontend
                            if last_msg["role"] == "ai":
                                await websocket.send_json({
                                    "type": "ai_response",
                                    "payload": last_msg["content"]
                                })
                            current_state.update(values)

    except WebSocketDisconnect:
        print(f"--- Client {client_id} Disconnected ---")