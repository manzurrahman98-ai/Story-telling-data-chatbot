# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     # Database
#     DB_HOST = os.getenv("DB_HOST", "localhost")
#     DB_PORT = os.getenv("DB_PORT", "5432")
#     DB_NAME = os.getenv("DB_NAME", "ecommerce_db")
#     DB_USER = os.getenv("DB_USER", "postgres")
#     DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

#     # OpenAI
#     OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#     OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

#     # Security
#     MAX_ROWS_LIMIT = int(os.getenv("MAX_ROWS_LIMIT", "100"))
#     QUERY_TIMEOUT_SECONDS = int(os.getenv("QUERY_TIMEOUT_SECONDS", "30"))

#     # API
#     API_PORT = int(os.getenv("API_PORT", "8000"))


import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Explicitly find the .env file relative to this file's location
# This ensures it works even if you run the app from different folders
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "ecommerce_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "1122") # Matches your .env

    # Google Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    # 2. Add a print statement here temporarily to debug
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    # Security
    MAX_ROWS_LIMIT = int(os.getenv("MAX_ROWS_LIMIT", "100"))
    QUERY_TIMEOUT_SECONDS = int(os.getenv("QUERY_TIMEOUT_SECONDS", "30"))

    # API
    API_PORT = int(os.getenv("API_PORT", "8000"))

# 3. Validation Check
if not Config.GEMINI_API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY not found in environment!")

# For debugging: This will show you exactly what name the app is using when it starts
print(f"🚀 Application starting with model: {Config.GEMINI_MODEL}")
