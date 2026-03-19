import asyncio
import discord
from discord import app_commands
from discord.ext import commands

from services.context_manager import get_context
from services.openrouter import get_ai_response
from services.logger import setup_logger

logger = setup_logger(__name__)

# Global lock — only one AI response is generated at a time.
# Requests that arrive while the lock is held are rejected with an ephemeral message.
_lock = asyncio.Lock()


class AICommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ai", description="Send a message to the AI.")
    @app_commands.describe(message="The message to send.")
    async def ai(self, interaction: discord.Interaction, message: str) -> None:
        # Try to acquire the lock without blocking. If it's already held,
        # tell the user the bot is busy and bail out.
        if _lock.locked():
            await interaction.response.send_message(
                "The bot is currently generating a response. Please try again in a moment.",
                ephemeral=True,
            )
            return

        async with _lock:
            # Defer the response immediately — API calls can take several seconds
            # and Discord requires an acknowledgement within 3 seconds.
            await interaction.response.defer()

            try:
                context = await get_context(interaction.channel)
                reply = await get_ai_response(context, message)
                await interaction.followup.send(reply)
                logger.info(f"Responded to '{message[:50]}' in #{interaction.channel.name}")
            except Exception:
                logger.exception("Error generating AI response")
                await interaction.followup.send(
                    "Something went wrong while generating a response. Please try again.",
                )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AICommands(bot))
