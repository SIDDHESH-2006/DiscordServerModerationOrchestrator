#!/usr/bin/env python3
"""
Discord Server Moderation Orchestrator
Runs both the FastAPI backend and Discord bot together
"""
import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# Load environment variables
load_dotenv("config/.env")

def run_bot():
    """Start the Discord bot"""
    from bot.main import main
    main()

def run_backend():
    """Start the FastAPI backend"""
    import uvicorn
    uvicorn.run("backend.api:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Discord Moderation Orchestrator")
    parser.add_argument(
        "--mode",
        choices=["bot", "backend", "both"],
        default="both",
        help="What to run: 'bot' (Discord), 'backend' (API), or 'both' (default)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "bot":
        print("🤖 Starting Discord Bot...")
        run_bot()
    elif args.mode == "backend":
        print("🚀 Starting FastAPI Backend on http://localhost:8000...")
        run_backend()
    elif args.mode == "both":
        print("🚀 Starting both Backend and Bot...")
        print("📝 Run this in separate terminals:")
        print("   Terminal 1: python main.py --mode backend")
        print("   Terminal 2: python main.py --mode bot")
        print("\nOr use 'python main.py --mode both' to start both (requires async setup)")
