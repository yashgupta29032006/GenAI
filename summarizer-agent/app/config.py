import os
import logging
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Structured Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}',
    stream=sys.stdout
)
logger = logging.getLogger("summarizer-agent")

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PORT = int(os.getenv("PORT", 8080))
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
    TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", 30))

    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY is not set!")
            raise ValueError("GEMINI_API_KEY environment variable is not set.")
        logger.info(f"Config initialized: model={cls.MODEL_NAME}, port={cls.PORT}, timeout={cls.TIMEOUT_SECONDS}s")

config = Config()
