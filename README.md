# discord-ai-bot

A Discord bot that uses an AI model via [OpenRouter](https://openrouter.ai) to role-play as a custom character in your server. The bot reads recent channel history to maintain context and sends a message to the channel in-character when prompted.

## Prerequisites

- Python 3.10+
- A Discord bot token
- An OpenRouter API key

## 1. Set Up a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
2. Under **Bot**, click **Add Bot** and copy the token — you'll need it for the `.env` file.
3. Under **Bot**, enable the **Message Content Intent** (required for reading messages).
4. Under **OAuth2 → URL Generator**, select the `bot` and `applications.commands` scopes, then the permissions your bot needs (at minimum: **Send Messages**, **Read Message History**, **Manage Messages** for `/purge`).
5. Use the generated URL to invite the bot to your server.
6. For any private or restricted channel you want the bot to work in, go to that channel's settings → **Permissions** and grant the bot (or its role) **View Channel** access. By default, bots can only see channels visible to `@everyone`.

## 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_discord_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key

# Optional — defaults shown below
OPENROUTER_MODEL=deepseek/deepseek-v3.2
CONTEXT_WINDOW_SIZE=60
LOG_LEVEL=INFO
```

Recommended model to use is Claude Sonnet 4.5/4.6, but that can get pricy. Deepseek is a good and cheap alternative.

## 3. Write Your Character

Create a file called `character.txt` to define your bot's personality, rules, and example dialog. This file is used as the system prompt for every AI request. A pre-filled example is provided in `characterSAMPLE.txt` for reference.

The file can contain anything — a name, personality traits, speech rules, backstory, and example conversations. The more specific you are, the more consistent the character will be.

## 4. Install Dependencies & Run

```bash
# Activate the virtual environment
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# Install dependencies (first time only)
pip install -r requirements.txt

# Start the bot
python bot.py
```

## Commands

| Command | Description |
|---|---|
| `!ai <message>` | Send a message to the AI character. The bot reads recent channel history for context before replying. |
| `/purge <amount>` | Delete the last N messages in the channel. Requires **Manage Messages** permission. |
| `!sync` | Sync slash commands to the current server. Owner only. |
<img width="644" height="477" alt="Screenshot 2026-03-23 170123" src="https://github.com/user-attachments/assets/4b18c93f-82d1-48fc-aaad-823d11f61a76" />
