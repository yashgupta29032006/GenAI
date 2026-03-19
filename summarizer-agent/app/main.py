from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .agent import SummarizerAgent
from .config import config, logger
import uvicorn

app = FastAPI(title="AI Summarizer Agent", version="1.0.0")

# Request Model
class SummarizeRequest(BaseModel):
    text: str

# Response Model
class SummarizeResponse(BaseModel):
    summary: str
    status: str

# Initialize the agent
try:
    config.validate()
    # Note: Agent initialization might be deferred or handled in a lifespan event
except Exception as e:
    logger.error(f"Configuration validation failed: {str(e)}")

agent = SummarizerAgent()

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Input text is required.")
    
    if len(request.text) > 5000:
        logger.warning("Large text input received, processing...")
    
    try:
        summary = await agent.summarize(request.text)
        return SummarizeResponse(summary=summary, status="success")
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error during summarization.")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)
