from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from .agent import SummarizerAgent
from .config import config, logger
import uvicorn
import time

# Initialize FastAPI with metadata
app = FastAPI(
    title="AI Summarizer Agent (Production)",
    description="A production-ready AI summarizer agent powered by Gemini and ADK.",
    version="1.1.0"
)

# Request Model with Validation
class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="The original text to summarize.")

# Response Model
class SummarizeResponse(BaseModel):
    summary: str
    status: str
    processed_time_ms: float

# Singleton Agent (Lazy initialization if needed, but here simple)
agent = None

@app.on_event("startup")
async def startup_event():
    global agent
    try:
        config.validate()
        agent = SummarizerAgent()
        logger.info("Application startup complete.")
    except Exception as e:
        logger.critical(f"Startup failed: {str(e)}")
        # In production, you might want to exit or let health check fail
        # sys.exit(1)

# Global Error Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "status": "error"}
    )

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized.")
    
    start_time = time.time()
    try:
        summary = await agent.summarize(request.text)
        duration_ms = (time.time() - start_time) * 1000
        return SummarizeResponse(
            summary=summary, 
            status="success",
            processed_time_ms=round(duration_ms, 2)
        )
    except Exception as e:
        logger.error(f"Summarization error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Cloud Run Readiness/Liveness Check"""
    if agent is None:
        return JSONResponse(
            status_code=503, 
            content={"status": "unhealthy", "reason": "Agent not initialized"}
        )
    return {"status": "healthy", "model": config.MODEL_NAME}

if __name__ == "__main__":
    # This block allows running with 'python -m app.main'
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)
