import asyncio
import websockets
import json

async def test_interview():
    uri = "ws://localhost:8000/api/v1/ws/interview/test_user_1"
    
    print(f"Connecting to {uri}...")
    async with websockets.connect(uri) as websocket:
        print("✅ Connected!")

        # 1. Send Init (Upload Resume Trigger)
        print("\n--- Sending Resume Trigger ---")
        init_msg = {
            "type": "init",
            "payload": "sample_resume.pdf" # Ensure this file exists in root!
        }
        await websocket.send(json.dumps(init_msg))

        # 2. Listen for AI Response (Greeting + Q1)
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            
            if data["type"] == "ai_response":
                print(f"\n🤖 AI SAYS: {data['payload']}")
                
                # Check if it's a question (simple check for demo)
                if "?" in data["payload"]:
                    break # Stop after receiving the first question

        # 3. Send an Answer
        answer_text = "I would use MoveIt for motion planning and ros_control for the hardware interface."
        print(f"\n--- Sending Answer: '{answer_text}' ---")
        
        answer_msg = {
            "type": "answer",
            "payload": answer_text
        }
        await websocket.send(json.dumps(answer_msg))
        
        # 4. Listen for Q2
        response = await websocket.recv()
        data = json.loads(response)
        print(f"\n🤖 AI SAYS (Next Question): {data['payload']}")

if __name__ == "__main__":
    # Install websockets first: pip install websockets
    asyncio.run(test_interview())