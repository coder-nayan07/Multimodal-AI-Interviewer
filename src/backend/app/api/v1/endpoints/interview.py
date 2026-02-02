from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.backend.app.core.graph import app as interview_graph
import json

router = APIRouter()

@router.websocket("/ws/interview/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    print(f"--- Client {client_id} Connected ---")
    
    # Initialize an empty state for this session
    # In production, we would load this from Redis if the user reconnected
    current_state = {"messages": [], "current_question_index": 0}
    
    try:
        while True:
            # 1. Wait for User Input (Text or Resume trigger)
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # 2. Handle "Start Interview" (User sends Resume filename)
            if message["type"] == "init":
                print(f"Initializing with resume: {message['payload']}")
                current_state["resume_text"] = message["payload"]
                
                # Run Graph: Init -> Ask Question 1
                # We use astream to get the events step-by-step
                async for event in interview_graph.astream(current_state):
                    for node, values in event.items():
                        if "messages" in values:
                            # Send the AI's question to the Frontend
                            ai_msg = values["messages"][-1]["content"]
                            await websocket.send_json({
                                "type": "ai_response",
                                "payload": ai_msg
                            })
                            # Update our local state
                            current_state.update(values)

            # 3. Handle "User Answer" (User answers a question)
            elif message["type"] == "answer":
                print(f"Received Answer: {message['payload']}")
                
                # Append user answer to state
                # Note: In a real app, we'd append to 'messages' list properly
                
                # Run Graph: Process Answer -> Ask Next Question
                async for event in interview_graph.astream(current_state):
                     for node, values in event.items():
                        if "messages" in values:
                            ai_msg = values["messages"][-1]["content"]
                            await websocket.send_json({
                                "type": "ai_response",
                                "payload": ai_msg
                            })
                            current_state.update(values)

    except WebSocketDisconnect:
        print(f"--- Client {client_id} Disconnected ---")