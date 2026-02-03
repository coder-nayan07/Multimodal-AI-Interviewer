import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles # <--- NEW IMPORT
from fastapi.middleware.cors import CORSMiddleware
from src.backend.app.core.config import settings
from src.backend.app.api.v1.endpoints import interview

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

ABSOLUTE_STATIC_DIR = "~/nayan/Multimodal-Ai-Interviewer/static"

# Ensure it exists
os.makedirs(os.path.join(ABSOLUTE_STATIC_DIR, "audio"), exist_ok=True)

# Mount it
# This means: http://localhost:8000/static -> /home/dgx959/.../static
app.mount("/static", StaticFiles(directory=ABSOLUTE_STATIC_DIR), name="static")

print(f"SERVING FILES FROM: {ABSOLUTE_STATIC_DIR}")

# --- 2. CORS (Existing) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the WebSocket Router
app.include_router(interview.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy", "project": settings.PROJECT_NAME}

if __name__ == "__main__":
    import uvicorn
    # Hot Reload enabled for rapid dev
    uvicorn.run("src.backend.app.main:app", host="0.0.0.0", port=8000, reload=True)