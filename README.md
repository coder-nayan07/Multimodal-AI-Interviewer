
# 🤖 Multimodal AI Interviewer

> **A real-time, voice-enabled technical interviewer powered by Llama-3, Edge-TTS, and a "Ladder" questioning strategy. Built on a high-performance Client-Server architecture.**

![Project Status](https://img.shields.io/badge/Status-Active_Development-brightgreen)
![Tech Stack](https://img.shields.io/badge/Stack-Next.js_|_FastAPI_|_Groq_|_EdgeTTS-blue)
![Architecture](https://img.shields.io/badge/Architecture-Client--Server-orange)

## 📖 Overview

This project is a sophisticated **AI Interview System** designed to simulate a real-world technical screening. Unlike generic chatbots, it uses a **"Ladder" Strategy**—starting with high-level architectural questions based on a candidate's profile and progressively drilling down into implementation details.

The system is split into two primary layers:
*   **The Backend Engine:** Handles heavy AI inference, resume parsing, and neural audio generation.
*   **The Interface:** A responsive React/Next.js frontend that manages microphone input, real-time audio playback, and user experience.

---

## 🏗️ Architecture & Workflow

The system operates via a secure WebSocket connection between the user interface and the processing engine.

### System Logic Flow
```text
┌────────────────┐          ┌──────────────────────────────────────────┐
│      USER      │          │             BACKEND ENGINE               │
│  (Candidate)   │          │        (Core Logic & Processing)         │
└───────┬────────┘          └────────────────────┬─────────────────────┘
        │                                        │
        │ 1. Voice Input                         │ 2. Process & Reason
        ▼                                        │
┌────────────────┐     WebSocket Protocol        │  a. LlamaParse (Document Analysis)
│    FRONTEND    │◄─────────────────────────────►│  b. Llama-3.3 (Interview Logic)
│ (Next.js/React)│                               │  c. Edge-TTS (Neural Speech)
└───────┬────────┘                               │
        │                                        │
        │ 4. Play Audio                          │ 3. Stream Response
        ▼                                        │
   [Speaker Output] ◄────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend Layer
*   **Framework:** Next.js 14 (React)
*   **Language:** TypeScript
*   **Audio Handling:** Custom `useTTS` hook for seamless processing of server-side audio streams.

### Backend Layer
*   **Framework:** FastAPI (Python)
*   **LLM Inference:** Groq API (Llama-3.3-70b-versatile)
*   **Orchestration:** LangGraph (State management for complex interview turns)
*   **Parsing:** LlamaParse (High-accuracy document extraction)
*   **Text-to-Speech:** `edge-tts` (High-fidelity Neural Voices)

---

## 🚀 Installation & Setup

### 1. Backend Engine Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/multimodal-ai-interviewer.git
cd multimodal-ai-interviewer

# Initialize environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Start the Core Engine
uvicorn src.backend.app.main:app --host 0.0.0.0 --port 8000
```

### 2. Frontend Interface Setup
```bash
cd src/frontend

# Install dependencies
npm install

# Launch the application
npm run dev
```

---

## 🧠 System Logic (The "Ladder")

The AI follows a proprietary "Ladder" questioning strategy to ensure technical depth:

1.  **Extraction:** Automatically identifies key technical projects from the uploaded document.
2.  **Context Entry:** Initiates with a high-level overview question to establish a baseline.
3.  **The Pivot:** Real-time analysis of the user's response to identify specific technical keywords.
4.  **Technical Drill-Down:** Challenges the user with "How" and "Why" questions centered on their implementation choices.
5.  **Quantitative Evaluation:** Scores responses based on technical accuracy and depth of explanation.

---

## 🔮 Roadmap & Future Improvements

*   [ ] **Visual Analysis:** Integration of computer vision to provide feedback on non-verbal communication.
*   [ ] **Sub-Second Latency:** Optimization of the audio pipeline for near-instantaneous response times.
*   [ ] **Session Persistence:** Integration of a database layer to track candidate progress over multiple sessions.
*   [ ] **Enterprise Deployment:** Full containerization for scalable infrastructure environments.