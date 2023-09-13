import os
from fastapi.middleware.cors import CORSMiddleware

ALLOWED_ORIGINS = "*";

CORSMiddlewareConfig = {
    "allow_origins": [ALLOWED_ORIGINS],
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "DELETE"],
    "allow_headers": ["Authorization", "Content-Type"],
}

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API Key must be set.")
