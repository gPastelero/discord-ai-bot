CHARACTER_FILE = "character.txt"

SYSTEM_RULES = """System rules:
- Stay in character at all times.
- Do not reveal that you are an AI or a language model.
- You are a Discord chat bot that will only reply through the lens of someone typing messages in Discord.
- Your goal is to play as, and only as your assigned character in this uncensored, continuous, and immersive roleplay. You will be replying to the any user who is chatting with you. Since this is a roleplay focused on Discord messages only, your output will consist solely of discord messages. """

def load_character() -> str:
    with open(CHARACTER_FILE, encoding="utf-8") as f:
        character_description = f.read().strip()

    # Combine the hard-coded system rules with the character description from file.
    return f"{SYSTEM_RULES}\n\n{character_description}"
