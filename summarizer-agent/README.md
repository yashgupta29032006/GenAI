# AI Summarizer Agent (ADK + FastAPI + Cloud Run)

A production-ready AI agent built with Google ADK (Agent Development Kit), Gemini, and FastAPI, designed for simple and reliable text summarization.

## Features
- **ADK-powered Agent**: Uses Google ADK for structured AI interactions.
- **FastAPI**: Modern, fast (high-performance) web framework.
- **Gemini Integration**: Optimized for Google's Gemini models.
- **Cloud Run Ready**: Fully dockerized and compatible with Google Cloud Run.
- **Modular Design**: Clean separation of configuration, agent logic, and API.

## Project Structure
```text
summarizer-agent/
├── app/
│   ├── __init__.py
│   ├── main.py        # API implementation
│   ├── agent.py       # AI Agent logic using ADK
│   └── config.py      # Configuration and logging
├── tests/
│   └── test_api.py    # Request-based test script
├── Dockerfile         # Containerization script
├── requirements.txt   # Dependencies
├── .env.example       # Environment template
└── README.md          # Documentation
```

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- Docker (optional, for local container testing)
- Google Cloud CLI (for deployment)
- Gemini API Key ([Get it here](https://aistudio.google.com/))

### 2. Local Installation
```bash
# Clone or move into the project directory
cd summarizer-agent

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and paste your GEMINI_API_KEY
```

### 3. Running Locally
```bash
# Start the server
python -m app.main
```
The server will start on `http://localhost:8080`.

## Testing Steps

### 1. Automated Test Script
While the server is running, execute:
```bash
python tests/test_api.py
```

### 2. Manual Test with curl
```bash
curl -X POST http://localhost:8080/summarize \
     -H "Content-Type: application/json" \
     -d '{"text": "AI is changing the world by automating tasks and improving efficiency."}'
```

---

## Deployment to Google Cloud Run

### 1. Set Google Cloud Project
```bash
gcloud config set project [YOUR_PROJECT_ID]
```

### 2. Build and Push Container (Artifact Registry)
```bash
# Create a repository (if not exists)
gcloud artifacts repositories create summarizer-repo --repository-format=docker --location=us-central1

# Build and Push
gcloud builds submit --tag us-central1-docker.pkg.dev/[PROJECT_ID]/summarizer-repo/agent:latest .
```

### 3. Deploy to Cloud Run
```bash
gcloud run deploy summarizer-agent \
  --image us-central1-docker.pkg.dev/[PROJECT_ID]/summarizer-repo/agent:latest \
  --set-env-vars GEMINI_API_KEY=[YOUR_API_KEY] \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

---

## API Specification

### POST `/summarize`
**Input:**
```json
{
  "text": "Your long text here..."
}
```

**Output:**
```json
{
  "summary": "Condensed version of text...",
  "status": "success"
}
```

## Example Responses

### Success Case
```json
{
  "summary": "AI is revolutionizing industries by increasing productivity and enhancing human capabilities.",
  "status": "success"
}
```

### Error Case (400 Bad Request)
```json
{
  "detail": "Input text is required."
}
```
