from typing import List
from pydantic import BaseModel

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
    