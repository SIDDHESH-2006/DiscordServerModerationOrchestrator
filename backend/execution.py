import httpx
from config.settings import DISCORD_BOT_TOKEN, DISCORD_API_BASE

# Header required for all Discord API requests
def get_headers():
    if not DISCORD_BOT_TOKEN:
        # Used during unit tests (mocked HTTP)
        return {"Content-Type": "application/json"}

    return {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
HEADERS = get_headers()
async def get_roles(guild_id: int, client: httpx.AsyncClient) -> list:
    """
    Fetch all roles from a Discord guild.
    """
    url = f"{DISCORD_API_BASE}/guilds/{guild_id}/roles"
    response = await client.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()
def find_by_name(items: list, name: str):
    """
    Find an item (role/channel) by its name, case-insensitive.
    Returns the item dict if found, otherwise None.
    """
    name = name.lower()

    for item in items:
        if item.get("name", "").lower() == name:
            return item

    return None


async def create_role(guild_id: int, payload: dict, client: httpx.AsyncClient) -> dict:
    """
    Create a role in a Discord guild.
    If the role already exists, return the existing role.
    """

    # Step 1: Get existing roles
    roles = await get_roles(guild_id, client)

    # Step 2: Check for duplicates
    existing = find_by_name(roles, payload.get("name"))
    if existing:
        return {
            "status": "exists",
            "id": existing["id"],
            "name": existing["name"]
        }

    # Step 3: Prepare payload - set default permissions for admin roles
    if "admin" in payload.get("name", "").lower() and "permissions" not in payload:
        payload["permissions"] = 8

    # Step 4: Send request to create a new role
    url = f"{DISCORD_API_BASE}/guilds/{guild_id}/roles"
    response = await client.post(url, headers=get_headers(), json=payload)
    response.raise_for_status()

    created = response.json()

    # Step 5: Return clean structure
    return {
        "status": "created",
        "id": created["id"],
        "name": created["name"]
    }
async def get_channels(guild_id: int, client: httpx.AsyncClient) -> list:
    """
    Fetch all channels from a Discord guild.
    """
    url = f"{DISCORD_API_BASE}/guilds/{guild_id}/channels"
    response = await client.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()
async def create_channel(guild_id: int, payload: dict, client: httpx.AsyncClient) -> dict:
    """
    Create a channel in a Discord guild.
    If the channel already exists, return the existing channel.
    """

    # Step 1: Get existing channels
    channels = await get_channels(guild_id, client)

    # Step 2: Check for duplicates
    existing = find_by_name(channels, payload.get("name"))
    if existing:
        return {
            "status": "exists",
            "id": existing["id"],
            "name": existing["name"]
        }

    # Step 3: Prepare payload - convert type string to Discord integer
    # Discord channel types: 0=text, 1=DM, 2=voice, 3=group DM, 4=category, 5=announcement, 10=announcement thread, 11=public thread, 12=private thread
    channel_type_map = {
        "text": 0,
        "voice": 2,
        "category": 4,
        "announcement": 5
    }
    
    prepared_payload = {
        "name": payload.get("name"),
    }
    
    # Convert type string to integer if provided
    if "type" in payload and payload["type"]:
        channel_type_str = payload["type"]
        prepared_payload["type"] = channel_type_map.get(channel_type_str, 0)  # Default to text if unknown
    
    # Add optional fields if provided
    if payload.get("topic"):
        prepared_payload["topic"] = payload["topic"]
    
    # Handle category - convert category name to parent_id
    if payload.get("category"):
        category_name = payload["category"]
        # Find the category by name
        category = find_by_name(channels, category_name)
        if category:
            prepared_payload["parent_id"] = category["id"]
            print(f"   📁 Found category '{category_name}' with ID {category['id']}")
        else:
            print(f"   ⚠️  Category '{category_name}' not found, creating without category")
    
    print(f"   📦 Prepared Discord API payload: {prepared_payload}")

    # Step 4: Send request to create a new channel
    url = f"{DISCORD_API_BASE}/guilds/{guild_id}/channels"
    print(f"   🔗 POST {url}")
    response = await client.post(url, headers=get_headers(), json=prepared_payload)
    
    if response.status_code != 201:
        print(f"   ❌ Discord API returned {response.status_code}: {response.text}")
    
    response.raise_for_status()

    created = response.json()

    # Step 5: Return clean structure
    return {
        "status": "created",
        "id": created["id"],
        "name": created["name"]
    }
async def delete_role(guild_id: int, role_name: str, client: httpx.AsyncClient) -> dict:
    roles = await get_roles(guild_id, client)
    role = find_by_name(roles, role_name)

    if not role:
        return {
            "status": "role_not_found",
            "name": role_name
        }

    url = f"{DISCORD_API_BASE}/guilds/{guild_id}/roles/{role['id']}"
    response = await client.delete(url, headers=get_headers())
    response.raise_for_status()

    return {
        "status": "role_deleted",
        "name": role_name
    }
async def delete_channel(guild_id: int, channel_name: str, client: httpx.AsyncClient) -> dict:
    channels = await get_channels(guild_id, client)
    channel = find_by_name(channels, channel_name)

    if not channel:
        return {
            "status": "channel_not_found",
            "name": channel_name
        }

    url = f"{DISCORD_API_BASE}/channels/{channel['id']}"
    response = await client.delete(url, headers=get_headers())
    response.raise_for_status()

    return {
        "status": "channel_deleted",
        "name": channel_name
    }

async def create_invite(
    guild_id: int,
    channel_name: str,
    max_uses: int,
    expires_in_minutes: int,
    client: httpx.AsyncClient
):
    # Step 1: Find the channel
    channels = await get_channels(guild_id, client)
    channel = find_by_name(channels, channel_name)

    if not channel:
        return {
            "status": "channel_not_found",
            "channel": channel_name
        }

    # Step 2: Create invite
    url = f"{DISCORD_API_BASE}/channels/{channel['id']}/invites"

    payload = {
        "max_uses": max_uses,
        "max_age": expires_in_minutes * 60
    }

    response = await client.post(
        url,
        headers=get_headers(),
        json=payload
    )
    response.raise_for_status()

    invite = response.json()

    return {
        "status": "invite_created",
        "channel": channel_name,
        "invite_url": f"https://discord.gg/{invite['code']}"
    }
async def remove_user(
    guild_id: int,
    user_id: int,
    client: httpx.AsyncClient
):
    """
    Remove (kick) a user from a Discord guild.
    """
    url = f"{DISCORD_API_BASE}/guilds/{guild_id}/members/{user_id}"
    response = await client.delete(url, headers=get_headers())
    response.raise_for_status()

    return {
        "status": "user_removed",
        "user_id": user_id
    }
async def ban_user(
    guild_id: int,
    user_id: int,
    client: httpx.AsyncClient
):
    """
    Ban a user from a Discord guild.
    """
    url = f"{DISCORD_API_BASE}/guilds/{guild_id}/bans/{user_id}"
    response = await client.put(url, headers=get_headers())
    response.raise_for_status()

    return {
        "status": "user_banned",
        "user_id": user_id
    }
async def unban_user(
    guild_id: int,
    user_id: int,
    client: httpx.AsyncClient
):
    """
    Unban a user from a Discord guild.
    """
    url = f"{DISCORD_API_BASE}/guilds/{guild_id}/bans/{user_id}"
    response = await client.delete(url, headers=get_headers())
    response.raise_for_status()

    return {
        "status": "user_unbanned",
        "user_id": user_id
    }
async def mute_user(
    guild_id: int,
    user_id: int,
    mute: bool,
    client: httpx.AsyncClient
):
    """
    Mute or unmute a user in a Discord guild.
    """
    url = f"{DISCORD_API_BASE}/guilds/{guild_id}/members/{user_id}"
    payload = {
        "mute": mute
    }
    response = await client.patch(url, headers=get_headers(), json=payload)
    response.raise_for_status()

    return {
        "status": "user_muted" if mute else "user_unmuted",
        "user_id": user_id
    }
def create_bot_invite_link(
    bot_client_id: str,
    permissions: int
):
    """
    Generate an OAuth2 invite link for a bot.
    """
    return {
        "status": "bot_invite_created",
        "invite_url": (
            "https://discord.com/oauth2/authorize"
            f"?client_id={bot_client_id}"
            f"&permissions={permissions}"
            "&scope=bot"
        )
    }
async def remove_bot_from_guild(
    guild_id: int,
    bot_user_id: int,
    client: httpx.AsyncClient
):
    url = f"{DISCORD_API_BASE}/guilds/{guild_id}/members/{bot_user_id}"

    response = await client.delete(
        url,
        headers=get_headers()
    )
    response.raise_for_status()

    return {
        "status": "bot_removed",
        "bot_user_id": bot_user_id
    }

async def get_member(guild_id: int, user_id: int, client: httpx.AsyncClient) -> dict:
    """
    Fetch a member from a Discord guild.
    """
    url = f"{DISCORD_API_BASE}/guilds/{guild_id}/members/{user_id}"
    response = await client.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()


async def get_ban(guild_id: int, user_id: int, client: httpx.AsyncClient) -> dict:
    """
    Fetch a ban object for a user in a guild.
    """
    url = f"{DISCORD_API_BASE}/guilds/{guild_id}/bans/{user_id}"
    response = await client.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()


async def add_role_to_member(
    guild_id: int,
    user_id: int,
    role_id: int,
    client: httpx.AsyncClient
) -> dict:
    """
    Add a role to a guild member.
    """
    url = f"{DISCORD_API_BASE}/guilds/{guild_id}/members/{user_id}/roles/{role_id}"
    response = await client.put(url, headers=get_headers())
    response.raise_for_status()
    
    return {
        "status": "role_added",
        "user_id": user_id,
        "role_id": role_id
    }


async def remove_role_from_member(
    guild_id: int,
    user_id: int,
    role_id: int,
    client: httpx.AsyncClient
) -> dict:
    """
    Remove a role from a guild member.
    """
    url = f"{DISCORD_API_BASE}/guilds/{guild_id}/members/{user_id}/roles/{role_id}"
    response = await client.delete(url, headers=get_headers())
    response.raise_for_status()
    
    return {
        "status": "role_removed",
        "user_id": user_id,
        "role_id": role_id
    }


async def get_guild(guild_id: int, client: httpx.AsyncClient) -> dict:
    """
    Fetch details about a guild.
    """
    url = f"{DISCORD_API_BASE}/guilds/{guild_id}"
    response = await client.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()
