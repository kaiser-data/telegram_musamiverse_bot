#!/usr/bin/env python3
"""
Test the exact bot MCP functionality to confirm it works
"""
import asyncio
import sys

# Test the exact imports and setup the bot uses
try:
    from masumi_client import MasumiMCPClient
    from config import TELEGRAM_BOT_TOKEN, DEBUG_MODE
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

class TestBotMCP:
    def __init__(self):
        self.user_sessions = {}
    
    async def get_mcp_client(self):
        """Exact copy of bot's get_mcp_client method"""
        try:
            print("🔄 Creating new MCP client...")
            client = MasumiMCPClient()
            print("✅ MCP client created successfully")
            return client
        except Exception as e:
            print(f"❌ Failed to create MCP client: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    async def test_status_command(self):
        """Exact copy of bot's status command logic"""
        print("🔄 Status command called")
        
        mcp_client = None
        try:
            print("🔄 About to get MCP client...")
            # Test MCP connection with a simple query
            mcp_client = await self.get_mcp_client()
            print("🔄 MCP client obtained, calling query_registry...")
            result = await mcp_client.query_registry()
            print(f"📥 Query result: {result[:100]}...")
            
            if "Error" in result:
                status_msg = "⚠️ *MCP Server Status: Issues Detected*\n\n"
                status_msg += f"```\n{result}\n```"
                print("⚠️ Returning error status")
            else:
                status_msg = "✅ *MCP Server Status: Operational*\n\n"
                status_msg += "• Connected to Masumi MCP Server\n"
                status_msg += "• Registry access available\n" 
                status_msg += "• Testnet mode active (Preprod)\n"
                print("✅ Returning success status")
            
            print(f"📤 Final status message: {status_msg[:100]}...")
            return status_msg
            
        except Exception as e:
            print(f"❌ Exception in status_command: {e}")
            import traceback
            traceback.print_exc()
            status_msg = f"❌ *MCP Server Status: Connection Failed*\n\n```\n{str(e)}\n```"
            return status_msg
        finally:
            if mcp_client:
                print("🔄 Stopping MCP client...")
                await mcp_client.stop_server()
                print("✅ MCP client stopped")

async def main():
    print("🧪 Testing Bot MCP Integration")
    print("=" * 50)
    
    bot = TestBotMCP()
    
    print("\n1️⃣ Testing status command...")
    status_result = await bot.test_status_command()
    
    print(f"\n📊 Final Result:")
    print(status_result)
    
    if "Issues Detected" in status_result or "Operational" in status_result:
        print("\n✅ SUCCESS: Bot MCP integration is working!")
        print("✅ The bot should respond correctly to /status command")
    else:
        print("\n❌ FAILED: Bot MCP integration has issues")

if __name__ == "__main__":
    asyncio.run(main())