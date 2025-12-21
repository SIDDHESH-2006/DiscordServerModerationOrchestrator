import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="config/.env")

def get_openai_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("Warning: OPENAI_API_KEY not found in environment.")
    return key
