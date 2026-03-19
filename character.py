CHARACTER_FILE = "character.txt"

SYSTEM_RULES = """System rules:
- Stay in character at all times.
- Do not reveal that you are an AI or a language model.
- Keep responses concise unless detail is specifically requested.
- Do not produce harmful, illegal, or explicit content."""

def load_character() -> str:
    with open(CHARACTER_FILE, encoding="utf-8") as f:
        character_description = f.read().strip()

    # Combine the hard-coded system rules with the character description from file.
    return f"{SYSTEM_RULES}\n\n{character_description}"
