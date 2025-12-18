import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from bot.handlers import setup_commands

# Load env vars
load_dotenv("config/.env")

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
APP_ID = int(os.getenv("DISCORD_APP_ID"))

if not TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN missing")
if not APP_ID:
    raise RuntimeError("DISCORD_APP_ID missing")

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    application_id=APP_ID
)

@bot.event
async def on_ready():
    setup_commands(bot)
    print(f"Bot logged in as {bot.user} (ID: {bot.user.id})")
    await bot.tree.sync()
    print("Slash commands synced.")

def main():
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
