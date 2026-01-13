#!/usr/bin/env python3
"""
Validation & Diagnostics Script
Run this to check if everything is set up correctly before running the bot
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_status(title: str, success: bool, message: str = ""):
    """Print a status line"""
    status = f"{Colors.GREEN}✓{Colors.RESET}" if success else f"{Colors.RED}✗{Colors.RESET}"
    print(f"{status} {Colors.BOLD}{title}{Colors.RESET}")
    if message:
        print(f"  {message}")

def print_header(text: str):
    """Print a section header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}\n")

def main():
    print_header("🔍 Discord Bot Validation & Diagnostics")
    
    all_good = True
    
    # 1. Check Python version
    print(f"Checking Python version...")
    version = sys.version_info
    py_ok = version.major >= 3 and version.minor >= 9
    print_status("Python 3.9+", py_ok, f"Found Python {version.major}.{version.minor}")
    all_good = all_good and py_ok
    
    # 2. Check .env file
    print(f"\nChecking .env configuration...")
    env_path = Path("config/.env")
    env_exists = env_path.exists()
    print_status(".env file exists", env_exists)
    
    if env_exists:
        load_dotenv("config/.env")
        
        # Check required variables
        required_vars = {
            "DISCORD_BOT_TOKEN": "Discord Bot Token",
            "DISCORD_APP_ID": "Discord Application ID",
            "OPENAI_API_KEY": "OpenRouter/OpenAI API Key",
            "BACKEND_URL": "Backend API URL (default: http://localhost:8000/execute)"
        }
        
        for var, desc in required_vars.items():
            value = os.getenv(var)
            is_set = bool(value and value.strip())
            print_status(f"{var}", is_set, f"{'Set' if is_set else 'Missing'}")
            
            # Show partial value (hide secrets)
            if is_set and var in ["DISCORD_BOT_TOKEN", "OPENAI_API_KEY"]:
                partial = value[:20] + "..." if len(value) > 20 else value
                print(f"     Value: {partial}")
            
            all_good = all_good and is_set
    
    # 3. Check project structure
    print(f"\nChecking project structure...")
    required_dirs = {
        "bot": "Bot implementation",
        "backend": "Backend API",
        "agent": "AI Agent",
        "config": "Configuration"
    }
    
    for dir_name, desc in required_dirs.items():
        dir_exists = Path(dir_name).is_dir()
        print_status(f"Directory: {dir_name}/", dir_exists, desc)
        all_good = all_good and dir_exists
    
    required_files = {
        "bot/main.py": "Bot entry point",
        "bot/handlers.py": "Discord command handlers",
        "backend/api.py": "FastAPI application",
        "agent/planner.py": "AI planning logic",
    }
    
    for file_path, desc in required_files.items():
        file_exists = Path(file_path).is_file()
        print_status(f"File: {file_path}", file_exists, desc)
        all_good = all_good and file_exists
    
    # 4. Check requirements
    print(f"\nChecking Python dependencies...")
    req_file = Path("requirements.txt")
    req_exists = req_file.exists()
    print_status("requirements.txt exists", req_exists)
    
    if req_exists:
        try:
            import discord
            print_status("discord.py", True, "✓ Installed")
        except ImportError:
            print_status("discord.py", False, "Not installed - run: pip install -r requirements.txt")
            all_good = False
        
        try:
            import fastapi
            print_status("fastapi", True, "✓ Installed")
        except ImportError:
            print_status("fastapi", False, "Not installed - run: pip install -r requirements.txt")
            all_good = False
        
        try:
            import langchain
            print_status("langchain", True, "✓ Installed")
        except ImportError:
            print_status("langchain", False, "Not installed - run: pip install -r requirements.txt")
            all_good = False
    
    # 5. Check API connectivity
    print(f"\nChecking backend connectivity...")
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000/execute")
    try:
        import requests
        response = requests.get("http://localhost:8000", timeout=2)
        backend_running = response.status_code == 200
        print_status("Backend API on localhost:8000", backend_running)
    except Exception as e:
        print_status("Backend API on localhost:8000", False, "Backend not running (start with: python main.py --mode backend)")
    
    # 6. Token validation
    print(f"\nValidating tokens...")
    bot_token = os.getenv("DISCORD_BOT_TOKEN", "")
    api_key = os.getenv("OPENAI_API_KEY", "")
    
    bot_token_valid = bot_token.startswith("MT") or bot_token.startswith("Nz")  # Discord tokens start with MT or Nz
    print_status("Discord Bot Token format", bot_token_valid, 
                 "Valid Discord token format" if bot_token_valid else "Token doesn't look like a Discord token")
    
    api_key_valid = api_key.startswith("sk-or-v1-") or api_key.startswith("sk-")
    print_status("OpenAI/OpenRouter API Key format", api_key_valid,
                 "Valid API key format" if api_key_valid else "Key doesn't look like OpenAI/OpenRouter key")
    
    # Final status
    print_header("📊 Summary")
    
    if all_good:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All checks passed!{Colors.RESET}")
        print(f"\nYou're ready to run the bot. Follow these steps:")
        print(f"\n{Colors.BOLD}1. Start the Backend:{Colors.RESET}")
        print(f"   python main.py --mode backend")
        print(f"\n{Colors.BOLD}2. Start the Bot (in another terminal):{Colors.RESET}")
        print(f"   python main.py --mode bot")
        print(f"\n{Colors.BOLD}3. Test in Discord:{Colors.RESET}")
        print(f"   /ping")
        print(f"   /orchestrate Create a moderation role")
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Some checks failed!{Colors.RESET}")
        print(f"\nFix the issues above, then run this script again.")
        print(f"\nNeed help? Check:")
        print(f"  - QUICKSTART.md")
        print(f"  - DISCORD_SETUP.md")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
