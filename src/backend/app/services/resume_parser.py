# import nest_asyncio
# nest_asyncio.apply()

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
        
        # Step B: IMPROVED "Ladder" Prompt
        task_prompt = f"""
        You are a friendly, Senior Technical Lead having a conversation with a future colleague.
        Your goal is to validate their depth of knowledge through curiosity, not interrogation.
        
        **YOUR STRATEGY (THE LADDER):**
        Instead of asking random trivia, find specific projects in the resume and ask "How" they built them.
        
        TASKS:
        1. **Extract Profile:** Who are they? (e.g., "A backend engineer focused on scalable Python systems").
        2. **Identify 3 Discussion Topics:** Find the 3 most interesting or complex projects/claims in their resume.
        3. **Generate 3 Technical Questions (The Climb):**
           - **Tone:** Generous and open. Use phrases like "I see you worked on X..." or "That sounds interesting..."
           - **Structure:** Start with the project context, then ask a specific implementation question.
           - **Example:** "I noticed you built a Chatbot using Redis. How did you handle message persistence if the Redis instance failed?" (Instead of "What is Redis?")
        4. **Generate 1 Behavioral Question:** Focus on learning or collaboration.
        
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