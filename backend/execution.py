import httpx
from config.settings import DISCORD_BOT_TOKEN, DISCORD_API_BASE

# Header required for all Discord API requests
HEADERS = {
    "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
    "Content-Type": "application/json"
}

async def get_roles(guild_id: int, client: httpx.AsyncClient) -> list:
    """
    Fetch all roles from a Discord guild.
    """
    url = f"{DISCORD_API_BASE}/guilds/{guild_id}/roles"
    response = await client.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()
