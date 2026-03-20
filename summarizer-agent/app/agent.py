import asyncio
import google.generativeai as genai
from .config import config, logger

class SummarizerAgent:
    def __init__(self):
        # Initialize Gemini directly with the stable SDK
        try:
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(config.MODEL_NAME)
            logger.info("SummarizerAgent initialized successfully using google-generativeai.")
        except Exception as e:
            logger.critical(f"Failed to initialize SummarizerAgent: {str(e)}")
            raise

    async def summarize(self, text: str) -> str:
        if not text.strip():
            logger.warning("Empty text received for summarization.")
            return "Error: Empty text provided."
        
        try:
            logger.info(f"Summarizing text (length: {len(text)})")
            # Use run_in_executor for standard generative-ai calls which are blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.model.generate_content(f"Summarize the following text:\n\n{text}")
            )
            return response.text
        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            raise e
