#!/usr/bin/env python3
"""
Test script to verify all imports and basic functionality work
"""
import sys
import os

print("🧪 Testing Bot Environment")
print("=" * 50)

print(f"📁 Current working directory: {os.getcwd()}")
print(f"🐍 Python path: {sys.executable}")
print(f"📦 Python path entries: {sys.path[:3]}...")

print("\n1️⃣ Testing basic imports...")
try:
    import asyncio
    from telegram import Update
    from telegram.ext import Application
    print("✅ Telegram imports OK")
except Exception as e:
    print(f"❌ Telegram import error: {e}")

print("\n2️⃣ Testing config import...")
try:
    from config import TELEGRAM_BOT_TOKEN, DEBUG_MODE
    print("✅ Config import OK")
    print(f"📊 DEBUG_MODE: {DEBUG_MODE}")
    print(f"🤖 Token length: {len(TELEGRAM_BOT_TOKEN) if TELEGRAM_BOT_TOKEN else 0}")
except Exception as e:
    print(f"❌ Config import error: {e}")
    import traceback
    traceback.print_exc()

print("\n3️⃣ Testing MCP client import...")
try:
    from masumi_client import MasumiMCPClient
    print("✅ MasumiMCPClient import OK")
except Exception as e:
    print(f"❌ MasumiMCPClient import error: {e}")
    import traceback
    traceback.print_exc()

print("\n4️⃣ Testing MCP client creation...")
try:
    client = MasumiMCPClient()
    print("✅ MCP client creation OK")
except Exception as e:
    print(f"❌ MCP client creation error: {e}")
    import traceback
    traceback.print_exc()

print("\n5️⃣ Testing async MCP operation...")
async def test_mcp():
    try:
        client = MasumiMCPClient()
        result = await client.query_registry()
        print(f"✅ MCP operation OK: {result[:50]}...")
        await client.stop_server()
        return True
    except Exception as e:
        print(f"❌ MCP operation error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    success = await test_mcp()
    print(f"\n📊 Overall result: {'✅ PASS' if success else '❌ FAIL'}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())