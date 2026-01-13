import os
from discord import app_commands, Interaction
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config/.env")

# Backend endpoint (default to localhost if not set)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/execute")

def setup_commands(bot):

    # -------------------------------
    # Ping command
    # -------------------------------
    @bot.tree.command(
        name="ping",
        description="Check if the bot is alive"
    )
    async def ping(interaction: Interaction):
        print(f"✅ PING command received from {interaction.user}")
        await interaction.response.send_message(
            "Pong! Bot is running.",
            ephemeral=True
        )
        print(f"✅ PING response sent")

    # -------------------------------
    # Orchestrate command
    # -------------------------------
    @bot.tree.command(
        name="orchestrate",
        description="Main entry command for server orchestration"
    )
    @app_commands.describe(request="Describe what you want to set up")
    async def orchestrate(interaction: Interaction, request: str):

        print(f"\n{'='*60}")
        print(f"📨 ORCHESTRATE command received")
        print(f"   User: {interaction.user}")
        print(f"   Guild: {interaction.guild}")
        print(f"   Request: {request}")
        print(f"{'='*60}")

        # Check permissions
        if interaction.guild and not interaction.user.guild_permissions.manage_guild:
            print(f"❌ User lacks 'manage_guild' permission")
            await interaction.response.send_message(
                "You need **Manage Server** permission to run this command.",
                ephemeral=True
            )
            return

        print(f"✅ Permissions verified, deferring response...")
        # Defer response (ephemeral)
        await interaction.response.defer(ephemeral=True)
        print(f"✅ Response deferred")

        # Prepare payload for backend
        payload = {
            "user_id": interaction.user.id,
            "guild_id": interaction.guild.id if interaction.guild else None,
            "content": request
        }

        print(f"📦 Payload: {payload}")

        try:
            # Use the REAL backend endpoint (not the test one)
            real_url = BACKEND_URL  # This is http://localhost:8000/execute
            print(f"🔗 Attempting to connect to: {real_url}")
            print(f"   Timeout: 60 seconds")
            
            async with httpx.AsyncClient(timeout=60, verify=False) as client:
                print(f"🔗 Sending POST request to REAL /execute endpoint...")
                response = await client.post(real_url, json=payload)
                print(f"✅ Response received with status: {response.status_code}")
                
                response.raise_for_status()
                data = response.json()
                print(f"✅ JSON parsed successfully")
                print(f"   Thought Process: {data.get('thought_process', 'N/A')[:100]}...")
                print(f"   Actions Count: {len(data.get('actions', []))}")
                print(f"   Final Response: {data.get('final_response', 'N/A')[:100]}...")

            # Send follow-up message
            final_response = data.get("final_response", "Request processed successfully.")
            print(f"📤 Sending followup message to Discord...")
            await interaction.followup.send(
                final_response,
                ephemeral=True
            )
            print(f"✅ Followup message sent!")
            print(f"{'='*60}\n")

        except httpx.ConnectError as e:
            error_msg = f"❌ Cannot connect to backend at {real_url}"
            print(f"{error_msg}: {str(e)}")
            await interaction.followup.send(error_msg, ephemeral=True)
        except httpx.TimeoutException as e:
            error_msg = f"❌ Backend request timed out after 60 seconds"
            print(f"{error_msg}")
            await interaction.followup.send(error_msg, ephemeral=True)
        except httpx.HTTPStatusError as e:
            error_msg = f"❌ Backend error ({e.response.status_code}): {e.response.text[:200]}"
            print(f"{error_msg}")
            await interaction.followup.send(error_msg, ephemeral=True)
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            print(f"{error_msg}")
            import traceback
            traceback.print_exc()
            await interaction.followup.send(error_msg, ephemeral=True)
        
        print(f"{'='*60}\n")
