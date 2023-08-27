# uvicorn main:app --reload
import os
import openai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.environ.get("OPENAI_API_KEY", "")

class Prompt(BaseModel):
    user_prompt: str

@app.post("/")
async def generate_reply(prompt: Prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": generate_prompt(prompt.user_prompt)}
        ]
    )
    generated_result = response['choices'][0]['message']['content'].strip()
    return {"generated_result": generated_result}

def generate_prompt(user_prompt: str) -> str:
    return user_prompt.capitalize()
