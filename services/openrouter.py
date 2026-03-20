import httpx
from character import load_character
from config import OPENROUTER_API_KEY, MODEL

LAST_OUTPUT_PATH = "logs/lastoutput.txt"


def _write_last_output(messages: list[dict], reply: str) -> None:
    lines = []
    for msg in messages:
        lines.append(f"[{msg['role'].upper()}]")
        lines.append(msg["content"])
        lines.append("")
    lines.append("[ASSISTANT REPLY]")
    lines.append(reply)
    with open(LAST_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def get_ai_response(context: list[dict], user_message: str, username: str = "User") -> str:
    """Send the conversation context and the new user message to OpenRouter
    and return the model's reply as a string."""

    messages = [
        # System prompt: rules + character description loaded from file.
        {"role": "system", "content": load_character()},
        # Prior channel history for context.
        *context,
        # The user's current message, prefixed with their username.
        {"role": "user", "content": f"{username}: {user_message}"},
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

    reply = response.json()["choices"][0]["message"]["content"]
    _write_last_output(messages, reply)
    return reply
