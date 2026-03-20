import os
import asyncio
import discord
from discord.ext import commands

from config import DISCORD_TOKEN
from services.logger import setup_logger

# Ensure the logs directory exists before the logger tries to create bot.log.
os.makedirs("logs", exist_ok=True)
logger = setup_logger()


class Bot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:
        await self.load_extension("cogs.ai_commands")
        await self.tree.sync()
        logger.info("Slash commands synced.")

    async def on_ready(self) -> None:
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")


async def main() -> None:
    async with Bot() as bot:
        await bot.start(DISCORD_TOKEN)


asyncio.run(main())
