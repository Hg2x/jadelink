import os
import openai
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
ALLOWED_ORIGINS = "http://localhost:3000/";

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API Key must be set.")

openai.api_key = OPENAI_API_KEY

class Prompt(BaseModel):
    user_prompt: str
    model: str

class Message(BaseModel):
    role: str
    content: str

class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class Response(BaseModel): # non-streamed response
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage

initial_chat_log = [{"role": "system", "content": "You are a helpful assistant."}]
chat_logs = initial_chat_log.copy() # TODO: still global, use database/session storage later

@app.post("/generate_reply")
async def generate_reply(prompt: Prompt):
    user_input = generate_prompt(prompt.user_prompt)
    chat_logs.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = openai.ChatCompletion.create(
            model=prompt.model,
            messages=chat_logs
        )
        validated_response = Response.parse_obj(response)
        generated_result = validated_response.choices[0].message.content.strip()
        prompt_tokens = validated_response.usage.prompt_tokens
        completion_tokens = validated_response.usage.completion_tokens 
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interacting with OpenAI API.")

    chat_logs.append({
        "role": "assistant",
        "content": generated_result
    })
    return {"chat_logs": chat_logs, "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens}

@app.delete("/chat_logs")
async def clear_chat():
    global chat_logs
    chat_logs = initial_chat_log.copy()  # copy() to make sure they're separate lists in memory
    return {"status": "Chat history cleared"}


@app.get("/chat_logs")
async def get_chat_logs():
    return {"chat_logs": chat_logs}

def generate_prompt(user_prompt: str) -> str:
    return user_prompt.capitalize()  # TODO: add more validation/sanitization here
