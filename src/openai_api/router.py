import openai
from fastapi import APIRouter, HTTPException
from .schemas import Prompt, Response
from .utils import generate_prompt

router = APIRouter()

initial_chat_log = [{"role": "system", "content": "You are a helpful assistant."}]
chat_logs = initial_chat_log.copy() # TODO: still global, use database/session storage later

@router.post("/generate_reply")
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

@router.delete("/chat_logs")
async def clear_chat():
    global chat_logs
    chat_logs = initial_chat_log.copy()  # copy() to make sure they're separate lists in memory
    return {"status": "Chat history cleared"}


@router.get("/chat_logs")
async def get_chat_logs():
    return {"chat_logs": chat_logs}
