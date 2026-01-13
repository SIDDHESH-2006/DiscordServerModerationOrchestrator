import os
import sys
from dotenv import load_dotenv
import discord
from discord.ext import commands
from bot.handlers import setup_commands

# --------------------------
# Load environment variables
# --------------------------
load_dotenv("config/.env")

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
APP_ID = os.getenv("DISCORD_APP_ID")

if not TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN is missing in .env")
if not APP_ID:
    raise RuntimeError("DISCORD_APP_ID is missing in .env")
APP_ID = int(APP_ID)

# --------------------------
# Setup intents
# --------------------------
intents = discord.Intents.default()
# Note: Privileged intents below - must be enabled in Discord Developer Portal
# Uncomment these if you enable them in the developer portal:
# intents.message_content = True
# intents.members = True

# --------------------------
# Create bot instance
# --------------------------
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    application_id=APP_ID
)

# --------------------------
# Bot ready event
# --------------------------
@bot.event
async def on_ready():
    print(f"🤖 Bot logged in as {bot.user} (ID: {bot.user.id})")
    # Setup commands AFTER bot is ready
    setup_commands(bot)
    # Sync slash commands
    await bot.tree.sync()
    print("✅ Slash commands synced and ready!")

# --------------------------
# Main function
# --------------------------
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--mode":
        mode = sys.argv[2] if len(sys.argv) > 2 else None
        if mode == "bot":
            print("🤖 Starting Discord Bot...")
            bot.run(TOKEN)
            return
        else:
            print(f"Unknown mode: {mode}")
            sys.exit(1)
    else:
        print("Usage: python main.py --mode bot")
        sys.exit(1)

# --------------------------
# Entry point
# --------------------------
if __name__ == "__main__":
    main()
