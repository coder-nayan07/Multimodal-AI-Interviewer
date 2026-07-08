

# 🤖 Multimodal AI Interviewer

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Llama-3](https://img.shields.io/badge/LLM-Llama--3.3--70B-orange.svg)](https://groq.com/)
[![Framework](https://img.shields.io/badge/Framework-LangChain-green.svg)](https://www.langchain.com/)

A real-time, voice-enabled technical interviewer that simulates a professional hiring process. Using a **"Ladder" questioning strategy**, the system analyzes a candidate's resume against a job description, plans a targeted interview, and conducts it with deep, evaluative follow-up questions.

> **Status:** 🚀 Core Orchestration Engine is Functional. Voice & Video modes are currently under development.

---

## 🌟 Key Features

-   **Deep Profile Analysis:** Automatically parses PDF/TXT resumes and Job Descriptions to identify skill gaps and discussion points.
-   **The "Ladder" Questioning Strategy:** Moves beyond simple Q&A. The engine generates an initial question and then uses a `FollowUpGenerator` to probe deeper based on the candidate's specific answers.
-   **Deterministic Interview Engine:** A robust state machine that manages session flow, topic transitions, and turn-taking without LLM "hallucinations" in the workflow logic.
-   **Structured Evaluation:** Every answer is evaluated against specific checkpoints to determine if the candidate demonstrated "Excellent," "Good," "Partial," or "Poor" understanding.
-   **Professional Reporting:** Generates a final JSON/Object-based report including strengths, weaknesses, and a final hiring recommendation (Strong Hire to No Hire).

---

## 🛠️ Tech Stack

-   **LLM:** Llama-3.3-70B-Versatile via **Groq** (Ultra-low latency inference).
-   **Orchestration:** LangChain & Pydantic (Structured Output).
-   **Parsing:** PyMuPDF (fitz) for high-accuracy PDF text extraction.
-   **Architecture:** Modular Domain-Driven Design (Parsers, Profilers, Planners, Evaluators).

---

## 📂 Project Structure

```text
├── src/
│   ├── evaluation/     # Answer logic & checkpoint verification
│   ├── interview/      # Deterministic session management
│   ├── llm/            # LLM Clients & specialized prompts
│   ├── models/         # Pydantic schemas (The "Source of Truth")
│   ├── parsers/        # Resume & JD PDF/TXT processing
│   ├── planning/       # Interview topic & strategy generation
│   ├── profiling/      # Candidate vs. JD gap analysis
│   ├── questioning/    # Question & Follow-up logic
│   └── reporting/      # Final interview summary generation
├── data/               # Resumes and JDs for testing
└── main.py             # CLI Entry point
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- A Groq API Key (Sign up at [console.groq.com](https://console.groq.com/))

### 2. Installation
```bash
git clone https://github.com/coder-nayan07/multimodal-ai-interviewer.git
cd multimodal-ai-interviewer
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the Interview (CLI Mode)
Place your resume (PDF) and JD (TXT) in the `data/` folder, update the paths in `main.py`, and run:
```bash
python main.py
```

---

## 🏗️ How the "Ladder" Strategy Works

The engine doesn't just ask random questions. It follows a structured cognitive path:
1.  **Initial Question:** Asks a broad but focused technical question based on the resume/JD context.
2.  **Evaluation:** The `AnswerEvaluator` checks the response against `answer_checkpoints`.
3.  **The Pivot:** 
    *   If the answer is sufficient, it advances to the **Next Topic**.
    *   If the answer shows partial understanding, the `FollowUpGenerator` creates a targeted probe to dig deeper into the missing concepts.
4.  **Completion:** Once all topics are exhausted, a comprehensive hiring report is synthesized.

---

## 🔮 Roadmap: The Multimodal Shift

We are currently transitioning from a CLI-based tool to a fully immersive multimodal experience:

*   **🎙️ Voice Mode (Next):**
    *   **Text-to-Speech (TTS):** Using Edge-TTS to allow the interviewer to speak questions naturally.
    *   **Speech-to-Text (STT):** Allowing candidates to answer via microphone.
*   **🎥 Video Mode:**
    *   Integrating a visual interface to display an AI avatar and real-time transcription.
*   **🌐 Web Interface:**
    *   A FastAPI-powered frontend for a seamless browser-based interview experience.

---

## 🤝 Contributing

This project is under active development. If you're interested in the intersection of AI Agents and Recruitment Tech, feel free to fork, open issues, or submit PRs.

---

## 📄 License

[MIT](LICENSE) — Created by **Nayan** (coder-nayan07)