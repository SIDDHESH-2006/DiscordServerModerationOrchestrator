import discord
from discord import app_commands

def setup_commands(bot):

    @bot.tree.command(
        name="ping",
        description="Check if the bot is alive"
    )
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(
            "Pong! Bot is running.",
            ephemeral=True
        )

    @bot.tree.command(
        name="orchestrate",
        description="Main entry command for server orchestration"
    )
    @app_commands.describe(request="Describe what you want to set up")
    async def orchestrate(interaction: discord.Interaction, request: str):

        if interaction.guild and not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message(
                "You need **Manage Server** permission.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"Received request: `{request}`",
            ephemeral=True
        )
