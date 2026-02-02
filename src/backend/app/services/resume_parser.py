import nest_asyncio
nest_asyncio.apply()

from groq import Groq
import instructor
from llama_parse import LlamaParse
from typing import List

# Import our Config and State
from src.backend.app.core.config import settings
from src.backend.app.core.state import InterviewPlan, CandidateProfile, Question

class ResumeArchitect:
    def __init__(self):
        # --- FIXED: Changed Mode.JSON_SCHEMA to Mode.TOOLS ---
        self.client = instructor.from_groq(
            Groq(api_key=settings.GROQ_API_KEY),
            mode=instructor.Mode.TOOLS 
        )
        
        # 2. Initialize the PDF Parser
        self.parser = LlamaParse(
            api_key=settings.LLAMA_CLOUD_API_KEY,
            result_type="markdown", 
            verbose=True,
            language="en"
        )

    async def process_resume(self, file_path: str) -> InterviewPlan:
        """
        Reads a PDF and returns a Pydantic-validated Interview Plan.
        """
        print(f"--- [ResumeArchitect] Reading: {file_path} ---")
        
        # Step A: Parse PDF to Markdown
        documents = await self.parser.aload_data(file_path)
        resume_text = documents[0].text
        
        print("--- [ResumeArchitect] Parsing Complete. Extracting with Llama-3... ---")
        
        # Step B: LLM Extraction
        task_prompt = f"""
        You are an expert Technical Interviewer.
        Analyze the following resume text.
        
        TASKS:
        1. Extract the candidate's core profile.
        2. Identify their WEAKEST areas or vague claims.
        3. Generate 3 Technical questions specifically targeting those weak points.
        4. Generate 1 Behavioral question.
        
        RESUME CONTENT:
        {resume_text}
        """

        # Step C: Structured Generation
        plan = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a strict JSON output engine."},
                {"role": "user", "content": task_prompt}
            ],
            response_model=InterviewPlan,
            max_tokens=4000
        )
        
        return plan