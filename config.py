import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")

# MCP Server Configuration
MCP_SERVER_PATH = os.getenv("MCP_SERVER_PATH", "../masumi-mcp-server/server.py")
PYTHONPATH = os.getenv("PYTHONPATH", "../masumi-mcp-server/")

# Bot Settings
BOT_USERNAME = os.getenv("BOT_USERNAME", "MasumiTestBot")
DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"