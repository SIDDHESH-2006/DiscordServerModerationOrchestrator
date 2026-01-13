# Discord Server Moderation Orchestrator

Intelligent Discord bot that uses AI to automate server management tasks. Tell it what you want, and it automatically creates roles, channels, handles moderation, and more!

## Features

- **Natural Language Commands**: Just describe what you want ("Create a moderator role")
- **AI-Powered Planning**: Uses OpenAI/OpenRouter to understand your intent
- **Automated Execution**: Automatically creates roles, channels, manages permissions
- **Safe Operations**: All actions require "Manage Server" permission
- **Extensible**: Easy to add new action types

## Quick Start (5 minutes)

### 1. Prerequisites
- **Python 3.9+** - Download from https://python.org
- **Discord Bot Token** - Create at https://discord.com/developers/applications

### 2. Install & Configure

```bash
# Install dependencies
pip install -r requirements.txt

# Edit config/.env with your tokens
# DISCORD_BOT_TOKEN=your_token_here
# DISCORD_APP_ID=your_app_id_here
# OPENAI_API_KEY=your_api_key_here
```

### 3. Add Bot to Discord Server
1. Go to https://discord.com/developers/applications
2. Select your app → OAuth2 → URL Generator
3. Select: `bot`, `applications.commands`
4. Permissions: `Manage Roles`, `Manage Channels`, `Manage Guild`, `Send Messages`
5. Open the generated link to invite bot to your server

### 4. Run the Bot

**Terminal 1 - Backend API:**
```bash
python main.py --mode backend
```

**Terminal 2 - Discord Bot:**
```bash
python main.py --mode bot
```

### 5. Test It!

In Discord, type:
```
/ping
```

Then try:
```
/orchestrate Create a moderation team with a mod role and mod-log channel
```

## Complete Guides

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[DISCORD_SETUP.md](DISCORD_SETUP.md)** - Detailed Discord configuration steps
- **[validate.py](validate.py)** - Run to check if everything is set up

## How It Works

```
You in Discord
    ↓
/orchestrate "Create a mod role"
    ↓
Discord Bot (discord.py)
    ↓ (HTTP POST)
FastAPI Backend
    ↓
AI Agent (LangChain)
    ↓
Generates action plan
    ↓
Discord API (Creates role, channel, etc.)
    ↓
Result back to Discord
```

## Usage Examples

```
/orchestrate Create a moderation team with admin and mod roles
/orchestrate Ban user 123456789 for breaking rules
/orchestrate Create a private support channel
/orchestrate Archive inactive channels
```

## Setup Steps

1. **Create Discord Application**
   - Go to [Developer Portal](https://discord.com/developers/applications)
   - Create new app and bot
   - Copy `DISCORD_BOT_TOKEN` and `DISCORD_APP_ID` → `config/.env`

2. **Get API Key**
   - Go to [OpenRouter.ai](https://openrouter.ai) or [OpenAI](https://openai.com/api)
   - Create API key
   - Copy to `config/.env` as `OPENAI_API_KEY`

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Invite Bot to Server**
   - DevPortal → OAuth2 → URL Generator
   - Select `bot`, `applications.commands`
   - Permissions: `Manage Roles`, `Manage Channels`, `Manage Guild`, `Send Messages`
   - Open URL and select your server

5. **Run Backend** (Terminal 1)
   ```bash
   python main.py --mode backend
   ```

6. **Run Bot** (Terminal 2)
   ```bash
   python main.py --mode bot
   ```

7. **Test**
   ```
   /ping
   ```

## Validation

Check if everything is set up correctly:
```bash
python validate.py
```

## Project Structure

```
bot/              → Discord bot commands
backend/          → FastAPI API server
agent/            → AI planning logic
config/           → Settings & .env
main.py           → Entry point
validate.py       → Setup checker
requirements.txt  → Python packages
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Bot not responding | Check Terminal 2 is running, bot has permissions |
| "Failed to process request" | Check Terminal 1 backend is running |
| API key error | Verify key format: `sk-or-v1-` or `sk-` |
| Missing permissions | Move bot role above others in server roles |

## Dependencies

- `discord.py` - Bot framework
- `fastapi` - API server
- `langchain` - AI orchestration
- `openai` - LLM API
- `pydantic` - Data validation
- `httpx` - HTTP client
- `python-dotenv` - Environment config

## Next Steps

1. Run `python validate.py` - Check setup
2. Read [QUICKSTART.md](QUICKSTART.md) - Get started in 5 min
3. Follow [DISCORD_SETUP.md](DISCORD_SETUP.md) - Configure Discord
4. Run the bot!

---

**Let's automate your Discord server! 🎉**
