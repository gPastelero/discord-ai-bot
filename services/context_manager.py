import discord
from config import CONTEXT_LIMIT

async def get_context(channel: discord.TextChannel) -> list[dict]:
    """Fetch the last CONTEXT_LIMIT messages from a channel and return them
    formatted as a conversation history for the OpenRouter API."""

    messages = []

    # channel.history returns messages newest-first, so we reverse to get
    # chronological order for the API.
    async for message in channel.history(limit=CONTEXT_LIMIT):
        # Skip bot messages that aren't AI responses (e.g. ephemeral "busy" notices).
        if message.author.bot and not message.content:
            continue

        role = "assistant" if message.author.bot else "user"
        messages.append({"role": role, "content": message.content})

    messages.reverse()
    return messages
