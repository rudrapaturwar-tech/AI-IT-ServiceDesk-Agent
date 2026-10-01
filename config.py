import os
from dotenv import load_dotenv

# Find absolute path to .env file
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, '.env')

load_dotenv(dotenv_path=env_path, override=True)

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.groq.com/openai/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.1))