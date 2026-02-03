import edge_tts
import uuid
import os

VOICE = "en-US-ChristopherNeural"

# --- FIX: USE THE SAME ABSOLUTE PATH AS MAIN.PY ---
# Go up 3 levels from: src/backend/app/services/tts.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
AUDIO_DIR = os.path.join(BASE_DIR, "static", "audio")

async def generate_audio(text: str) -> str:
    # 1. Ensure directory exists
    os.makedirs(AUDIO_DIR, exist_ok=True)

    # 2. Generate filename
    filename = f"response_{uuid.uuid4()}.mp3"
    file_path = os.path.join(AUDIO_DIR, filename)
    
    # 3. Create audio
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(file_path)
    
    # 4. Return URL (This matches the mount in main.py)
    return f"/static/audio/{filename}"