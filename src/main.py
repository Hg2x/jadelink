from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .openai_api.config import CORSMiddlewareConfig, OPENAI_API_KEY
from .openai_api.router import router as openai_router
import openai

app = FastAPI()

app.include_router(openai_router)

app.add_middleware(
    CORSMiddleware,
    **CORSMiddlewareConfig
)

openai.api_key = OPENAI_API_KEY