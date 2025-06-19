#!/usr/bin/env python3
"""
Comprehensive bot issue diagnosis
"""
import os
import sys
import asyncio
from pathlib import Path

print("🔍 COMPREHENSIVE BOT DIAGNOSIS")
print("=" * 60)

# 1. Environment Check
print("\n1️⃣ ENVIRONMENT CHECK")
print(f"📁 Current working directory: {os.getcwd()}")
print(f"🐍 Python executable: {sys.executable}")
print(f"📦 Python version: {sys.version}")
print(f"🔧 Platform: {sys.platform}")

# 2. File System Check
print("\n2️⃣ FILE SYSTEM CHECK")
bot_py = Path("bot.py")
env_file = Path(".env")
masumi_client = Path("masumi_client.py")
config_py = Path("config.py")

print(f"📄 bot.py exists: {bot_py.exists()}")
print(f"📄 .env exists: {env_file.exists()}")
print(f"📄 masumi_client.py exists: {masumi_client.exists()}")
print(f"📄 config.py exists: {config_py.exists()}")

if env_file.exists():
    print(f"📄 .env size: {env_file.stat().st_size} bytes")

# 3. Import Test
print("\n3️⃣ IMPORT TEST")
try:
    import telegram
    print(f"✅ telegram: {telegram.__version__}")
except Exception as e:
    print(f"❌ telegram import failed: {e}")

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ dotenv loaded")
except Exception as e:
    print(f"❌ dotenv failed: {e}")

try:
    from config import TELEGRAM_BOT_TOKEN, DEBUG_MODE
    print(f"✅ config imported, DEBUG_MODE: {DEBUG_MODE}")
    print(f"✅ bot token length: {len(TELEGRAM_BOT_TOKEN) if TELEGRAM_BOT_TOKEN else 0}")
except Exception as e:
    print(f"❌ config import failed: {e}")

try:
    from masumi_client import MasumiMCPClient
    print("✅ MasumiMCPClient imported")
except Exception as e:
    print(f"❌ MasumiMCPClient import failed: {e}")
    import traceback
    traceback.print_exc()

# 4. Environment Variables Check
print("\n4️⃣ ENVIRONMENT VARIABLES")
env_vars = [
    "TELEGRAM_BOT_TOKEN",
    "MCP_SERVER_PATH", 
    "PYTHONPATH",
    "MASUMI_REGISTRY_TOKEN",
    "MASUMI_PAYMENT_TOKEN",
    "MASUMI_NETWORK",
    "MASUMI_REGISTRY_BASE_URL",
    "MASUMI_PAYMENT_BASE_URL"
]

for var in env_vars:
    value = os.getenv(var)
    if value:
        if "TOKEN" in var:
            print(f"🔑 {var}: ***{value[-4:]} (length: {len(value)})")
        else:
            print(f"🔑 {var}: {value}")
    else:
        print(f"❌ {var}: NOT SET")

# 5. MCP Server Path Check
print("\n5️⃣ MCP SERVER PATH CHECK")
mcp_path = os.getenv("MCP_SERVER_PATH")
if mcp_path:
    mcp_file = Path(mcp_path)
    print(f"📍 MCP server path: {mcp_path}")
    print(f"📄 MCP server exists: {mcp_file.exists()}")
    if mcp_file.exists():
        print(f"📄 MCP server size: {mcp_file.stat().st_size} bytes")
    
    # Test if we can import the server
    pythonpath = os.getenv("PYTHONPATH")
    if pythonpath and Path(pythonpath).exists():
        print(f"📁 PYTHONPATH exists: {pythonpath}")
        sys.path.insert(0, pythonpath)
        try:
            import server
            print("✅ MCP server module can be imported")
        except Exception as e:
            print(f"❌ MCP server import failed: {e}")
    else:
        print(f"❌ PYTHONPATH not found: {pythonpath}")

# 6. Quick MCP Test
print("\n6️⃣ QUICK MCP TEST")
try:
    client = MasumiMCPClient()
    print("✅ MCP client creation: SUCCESS")
except Exception as e:
    print(f"❌ MCP client creation: FAILED - {e}")
    import traceback
    traceback.print_exc()

# 7. Virtual Environment Check
print("\n7️⃣ VIRTUAL ENVIRONMENT CHECK")
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("✅ Running in virtual environment")
    print(f"📁 Virtual env: {sys.prefix}")
else:
    print("❌ NOT running in virtual environment")

print("\n" + "=" * 60)
print("🎯 DIAGNOSIS COMPLETE")
print("=" * 60)