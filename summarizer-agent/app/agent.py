from google import adk
from .config import config, logger

class SummarizerAgent:
    def __init__(self):
        # Initialize ADK with Gemini
        # Note: In a real production environment, you'd use the appropriate ADK initialization
        # For simplicity and following ADK patterns:
        self.agent = adk.LlmAgent(
            model=config.MODEL_NAME,
            api_key=config.GEMINI_API_KEY,
            instructions="You are a professional text summarizer. Provide concise and clear summaries of the provided text. Focus on the main points and key takeaways."
        )
        logger.info("SummarizerAgent initialized successfully.")

    async def summarize(self, text: str) -> str:
        if not text.strip():
            return "Error: Empty text provided."
        
        try:
            logger.info(f"Summarizing text: {text[:50]}...")
            # Use ADK's interaction method
            response = await self.agent.ask(f"Summarize the following text:\n\n{text}")
            return response.text
        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            raise e
