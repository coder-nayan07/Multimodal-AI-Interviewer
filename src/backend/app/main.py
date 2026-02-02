from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.app.core.config import settings
from src.backend.app.api.v1.endpoints import interview

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# CORS (Critical for connecting React later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local dev
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