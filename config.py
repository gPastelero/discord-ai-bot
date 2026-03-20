import os
from dotenv import load_dotenv

load_dotenv()

def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value

DISCORD_TOKEN: str = _require("DISCORD_TOKEN")
OPENROUTER_API_KEY: str = _require("OPENROUTER_API_KEY")

MODEL: str = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-v3.2")
CONTEXT_LIMIT: int = int(os.getenv("CONTEXT_WINDOW_SIZE", "60"))
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
