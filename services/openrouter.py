import httpx
from character import load_character
from config import OPENROUTER_API_KEY, MODEL

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def get_ai_response(context: list[dict], user_message: str) -> str:
    """Send the conversation context and the new user message to OpenRouter
    and return the model's reply as a string."""

    messages = [
        # System prompt: rules + character description loaded from file.
        {"role": "system", "content": load_character()},
        # Prior channel history for context.
        *context,
        # The user's current message.
        {"role": "user", "content": user_message},
    ]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": messages,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            OPENROUTER_URL, json=payload, headers=headers, timeout=60.0
        )
        response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
