# uvicorn main:app --reload
import os
import openai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.environ.get("OPENAI_API_KEY", "")

class Prompt(BaseModel):
    user_prompt: str

initial_chat_log = [{"role": "system", "content": "You are a helpful assistant."}]
chat_logs = initial_chat_log

@app.post("/")
async def generate_reply(prompt: Prompt):
    chat_logs.append({
        "role": "user",
        "content": generate_prompt(prompt.user_prompt)
    })

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_logs
    )
    generated_result = response['choices'][0]['message']['content'].strip()

    chat_logs.append({
        "role": "assistant",
        "content": generated_result
    })
    return {"generated_result": generated_result, "chat_logs": chat_logs}

@app.post("/clear_chat")
async def clear_chat():
    global chat_logs
    chat_logs = initial_chat_log
    return {"status": "Chat history cleared"}

def generate_prompt(user_prompt: str) -> str:
    return user_prompt.capitalize()
