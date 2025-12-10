"""
Configuration module for loading environment variables from .env file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# Load .env file from project root
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)


# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "")

