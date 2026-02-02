import asyncio
from src.backend.app.services.resume_parser import ResumeArchitect

async def test_parser():
    print("Initializing Architect...")
    architect = ResumeArchitect()
    print("Groq & LlamaParse Clients initialized successfully.")
    
    # If you have a resume, uncomment these lines to test the full flow:
    plan = await architect.process_resume("sample_resume.pdf")
    print(f"Candidate Identified: {plan.candidate.name}")

if __name__ == "__main__":
    asyncio.run(test_parser())