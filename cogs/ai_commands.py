import asyncio
import discord
from discord import app_commands
from discord.ext import commands

from services.context_manager import get_context
from services.openrouter import get_ai_response
from services.logger import setup_logger

logger = setup_logger(__name__)

# Global lock — only one AI response is generated at a time.
_lock = asyncio.Lock()


class AICommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="ai")
    async def ai(self, ctx: commands.Context, *, message: str) -> None:
        if _lock.locked():
            await ctx.send("The bot is currently generating a response. Please try again in a moment.")
            return

        async with _lock:
            async with ctx.typing():
                try:
                    context = await get_context(ctx.channel)
                    reply = await get_ai_response(context, message, ctx.author.display_name)
                    await ctx.send(reply)
                    logger.info(f"Responded to '{message[:50]}' in #{ctx.channel.name}")
                except Exception:
                    logger.exception("Error generating AI response")
                    await ctx.send("Something went wrong while generating a response. Please try again.")

    @app_commands.command(name="purge", description="Delete the last X messages in this channel.")
    @app_commands.describe(amount="Number of messages to delete.")
    @app_commands.default_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int) -> None:
        if amount < 1:
            await interaction.response.send_message("Amount must be at least 1.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"Deleted {len(deleted)} messages.", ephemeral=True)
        logger.info(f"{interaction.user} purged {len(deleted)} messages in #{interaction.channel.name}")


    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx: commands.Context) -> None:
        ctx.bot.tree.copy_global_to(guild=ctx.guild)
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(synced)} commands to this server.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AICommands(bot))
