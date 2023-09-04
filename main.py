# uvicorn main:app --reload
import os
import openai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API Key must be set.")

openai.api_key = OPENAI_API_KEY

class Prompt(BaseModel):
    user_prompt: str

initial_chat_log = [{"role": "system", "content": "You are a helpful assistant."}]
chat_logs = initial_chat_log # TODO: still global, consider using database/session storage

@app.post("/")
async def generate_reply(prompt: Prompt):
    user_input = generate_prompt(prompt.user_prompt)
    chat_logs.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_logs
        )
        generated_result = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interacting with OpenAI API.")

    chat_logs.append({
        "role": "assistant",
        "content": generated_result
    })
    return {"generated_result": generated_result, "chat_logs": chat_logs}

@app.post("/clear_chat")
async def clear_chat():
    global chat_logs
    chat_logs = initial_chat_log.copy()  # copy() to make sure they're separate lists in memory
    return {"status": "Chat history cleared"}

@app.get("/get_chat_logs")
async def get_chat_logs():
    return {"chat_logs": chat_logs}

def generate_prompt(user_prompt: str) -> str:
    return user_prompt.capitalize()  # TODO: add more validation/sanitization here

