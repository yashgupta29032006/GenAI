# AI Summarizer Agent (Production-Ready)

A high-performance, production-ready AI agent built with **Google ADK (Agent Development Kit)**, **Gemini**, and **FastAPI**. Designed for text summarization with robust error handling, structured logging, and Cloud Run compatibility.

## 🚀 Features
- **ADK-powered Agent**: Uses Google ADK for structured AI interactions.
- **FastAPI**: Modern, fast web framework with Pydantic validation.
- **Structured Logging**: JSON-formatted logs for production monitoring.
- **Timeouts**: AI calls are protected by timeouts to prevent hanging.
- **Readiness Checks**: Robust `/health` endpoint for Cloud Run.
- **Dockerized**: Optimized for Google Cloud Run (Port 8080).

## 📂 Project Structure
```text
summarizer-agent/
├── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI Implementation & Routes
│   ├── agent.py       # AI Agent logic using Google ADK
│   └── config.py      # Configuration, Logging & Timeouts
├── tests/
│   └── test_api.py    # Automated test script
├── Dockerfile         # Optimized container script
├── requirements.txt   # Dependencies
├── .env.example       # Environment template
└── README.md          # Documentation
```

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.10+
- Google Cloud CLI (for deployment)
- Gemini API Key ([Get it here](https://aistudio.google.com/))

### 2. Local Installation
```bash
cd summarizer-agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Set GEMINI_API_KEY in .env
```

### 3. Running Locally
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```
Server starts at `http://localhost:8080`.

## 🧪 Testing

### Automated Test
```bash
python tests/test_api.py
```

### Sample Manual Request (curl)
```bash
curl -X POST http://localhost:8080/summarize \
     -H "Content-Type: application/json" \
     -d '{"text": "Artificial Intelligence is transforming industries by automating tasks and providing deep insights from massive datasets."}'
```

### Expected JSON Response
```json
{
  "summary": "AI is revolutionizing industries through automation and data analysis.",
  "status": "success",
  "processed_time_ms": 1245.5
}
```

## ☁️ Deployment to Google Cloud Run

### 1. Build and Push to Artifact Registry
```bash
gcloud artifacts repositories create agent-repo --repository-format=docker --location=us-central1
gcloud builds submit --tag us-central1-docker.pkg.dev/[PROJECT_ID]/agent-repo/summarizer:latest .
```

### 2. Deploy to Cloud Run
```bash
gcloud run deploy summarizer-agent \
  --image us-central1-docker.pkg.dev/[PROJECT_ID]/agent-repo/summarizer:latest \
  --set-env-vars GEMINI_API_KEY=[YOUR_API_KEY] \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

**Final Service URL:** `https://summarizer-agent-64632696562.us-central1.run.app`

---
*Developed with ❤️ using ADK and FastAPI.*
