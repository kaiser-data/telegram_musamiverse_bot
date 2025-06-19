#!/usr/bin/env python3
"""
Test in the exact same environment as the bot to find the issue
"""
import asyncio
import sys
import os
import logging

# Set up the exact same logging as the bot
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

print("🔍 TESTING IN EXACT BOT ENVIRONMENT")
print("=" * 50)

print(f"🐍 Python: {sys.executable}")
print(f"📁 Working dir: {os.getcwd()}")
print(f"🔧 Virtual env: {'YES' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 'NO'}")

# Test imports exactly like bot.py
print("\n1️⃣ Testing imports...")
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
    from telegram.constants import ParseMode
    print("✅ Telegram imports OK")
except Exception as e:
    print(f"❌ Telegram imports failed: {e}")
    import traceback
    traceback.print_exc()

try:
    from masumi_client import MasumiMCPClient
    print("✅ MasumiMCPClient imported successfully")
except Exception as e:
    print(f"❌ Failed to import MasumiMCPClient: {e}")
    import traceback
    traceback.print_exc()

try:
    from config import TELEGRAM_BOT_TOKEN, DEBUG_MODE
    print("✅ Config imported successfully")
    print(f"📊 DEBUG_MODE: {DEBUG_MODE}")
    print(f"🤖 Token configured: {'Yes' if TELEGRAM_BOT_TOKEN else 'No'}")
except Exception as e:
    print(f"❌ Failed to import config: {e}")
    import traceback
    traceback.print_exc()

# Test MCP client creation and operation exactly like bot
print("\n2️⃣ Testing MCP client operations...")

class TestBot:
    def __init__(self):
        self.user_sessions = {}
    
    async def get_mcp_client(self):
        """Exact copy of bot's get_mcp_client method"""
        try:
            logger.info("🔄 Creating new MCP client...")
            client = MasumiMCPClient()
            logger.info("✅ MCP client created successfully")
            return client
        except Exception as e:
            logger.error(f"❌ Failed to create MCP client: {e}")
            import traceback
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
            raise

    async def test_status_like_bot(self):
        """Test exactly like bot's status command"""
        logger.info("🔄 Status command called by user")
        
        mcp_client = None
        try:
            logger.info("🔄 About to get MCP client...")
            mcp_client = await self.get_mcp_client()
            logger.info("🔄 MCP client obtained, calling query_registry...")
            result = await mcp_client.query_registry()
            logger.info(f"📥 Query result: {result[:100]}...")
            
            if "Error" in result:
                status_msg = "⚠️ *MCP Server Status: Issues Detected*\n\n"
                status_msg += f"```\n{result}\n```"
                logger.info("⚠️ Returning error status")
            else:
                status_msg = "✅ *MCP Server Status: Operational*\n\n"
                status_msg += "• Connected to Masumi MCP Server\n"
                status_msg += "• Registry access available\n" 
                status_msg += "• Testnet mode active (Preprod)\n"
                logger.info("✅ Returning success status")
            
            return status_msg
            
        except Exception as e:
            logger.error(f"❌ Exception in status_command: {e}")
            import traceback
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
            raise
        finally:
            if mcp_client:
                logger.info("🔄 Stopping MCP client...")
                await mcp_client.stop_server()
                logger.info("✅ MCP client stopped")

async def main():
    try:
        bot = TestBot()
        print("\n3️⃣ Testing status command...")
        
        result = await bot.test_status_like_bot()
        print(f"\n✅ SUCCESS: {result[:100]}...")
        
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        
        print(f"\n🔍 Error type: {type(e)}")
        print(f"🔍 Error args: {e.args}")

if __name__ == "__main__":
    asyncio.run(main())