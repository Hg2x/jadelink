# uvicorn main:app --reload
import os
import openai
from typing import Optional
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
openai.api_key = os.environ.get("OPENAI_API_KEY", "")
templates = Jinja2Templates(directory="templates/")

@app.get("/")
async def read_root(request: Request, result: Optional[str] = None):
    return templates.TemplateResponse("index.html", {"request": request, "result": result})

@app.post("/")
async def generate_reply(request: Request, user_prompt: str = Form(...)):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": generate_prompt(user_prompt)}
        ]
    )
    generated_result = response['choices'][0]['message']['content'].strip()
    return templates.TemplateResponse("index.html", {"request": request, "generated_result": generated_result})

def generate_prompt(user_prompt: str) -> str:
    return user_prompt.capitalize()
