from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class LLMClient:
    def __init__(
        self,
        model_name: str = "llama-3.3-70b-versatile",
        temperature: float = 0.0,
    ):
        self.llm = ChatGroq(
            model=model_name,
            temperature=temperature,
        )

    def get_llm(self):
        return self.llm