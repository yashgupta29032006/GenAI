import asyncio
from google import adk
from .config import config, logger

class SummarizerAgent:
    def __init__(self):
        # Initialize ADK with Gemini
        try:
            self.agent = adk.LlmAgent(
                model=config.MODEL_NAME,
                api_key=config.GEMINI_API_KEY,
                instructions="You are a professional text summarizer. Provide concise and clear summaries. Focus on main points."
            )
            logger.info("SummarizerAgent initialized successfully.")
        except Exception as e:
            logger.critical(f"Failed to initialize SummarizerAgent: {str(e)}")
            raise

    async def summarize(self, text: str) -> str:
        if not text.strip():
            logger.warning("Empty text received for summarization.")
            return "Error: Empty text provided."
        
        try:
            logger.info(f"Summarizing text (length: {len(text)})")
            # Use asyncio.wait_for to prevent hanging
            response = await asyncio.wait_for(
                self.agent.ask(f"Summarize the following text:\n\n{text}"),
                timeout=config.TIMEOUT_SECONDS
            )
            return response.text
        except asyncio.TimeoutError:
            logger.error(f"Summarization timed out after {config.TIMEOUT_SECONDS}s")
            raise Exception("AI model response timed out.")
        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            raise e
