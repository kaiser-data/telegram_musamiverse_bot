#!/usr/bin/env python3
"""
Debug script to test MCP client exactly as the bot uses it
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment exactly like the bot
print("🔧 Loading environment...")
load_dotenv()

print(f"📁 Current dir: {os.getcwd()}")
print(f"🔑 MASUMI_REGISTRY_TOKEN: {'✅ Set' if os.getenv('MASUMI_REGISTRY_TOKEN') else '❌ Missing'}")
print(f"🔑 MASUMI_PAYMENT_TOKEN: {'✅ Set' if os.getenv('MASUMI_PAYMENT_TOKEN') else '❌ Missing'}")
print(f"🌐 MASUMI_NETWORK: {os.getenv('MASUMI_NETWORK', 'Not set')}")
print(f"📍 MCP_SERVER_PATH: {os.getenv('MCP_SERVER_PATH', 'Not set')}")

# Import exactly like the bot
try:
    from masumi_client import MasumiMCPClient
    print("✅ MasumiMCPClient import successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    exit(1)

async def test_bot_workflow():
    """Test the exact workflow the bot uses"""
    print("\n🤖 Testing Bot MCP Workflow")
    print("=" * 50)
    
    # Step 1: Create client like bot does
    print("1️⃣ Creating MCP client...")
    try:
        client = MasumiMCPClient()
        print("✅ Client created")
    except Exception as e:
        print(f"❌ Client creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 2: Test query_registry like the /status command
    print("2️⃣ Testing query_registry (like /status command)...")
    try:
        result = await client.query_registry()
        print(f"📊 Result type: {type(result)}")
        print(f"📊 Result length: {len(str(result))}")
        print(f"📊 Result preview: {str(result)[:100]}...")
        
        if "Error" in result:
            print("⚠️ Got error result (expected for config issues)")
        else:
            print("✅ Got successful result")
            
    except Exception as e:
        print(f"❌ query_registry failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 3: Test list_agents
    print("3️⃣ Testing list_agents...")
    try:
        result = await client.list_agents()
        print(f"📊 List agents result: {str(result)[:100]}...")
    except Exception as e:
        print(f"❌ list_agents failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 4: Clean up
    print("4️⃣ Cleaning up...")
    try:
        await client.stop_server()
        print("✅ Client stopped successfully")
    except Exception as e:
        print(f"⚠️ Cleanup issue: {e}")
    
    return True

async def main():
    success = await test_bot_workflow()
    print(f"\n🎯 Overall result: {'✅ SUCCESS' if success else '❌ FAILED'}")
    
    if success:
        print("\n💡 MCP client is working! The bot should work too.")
        print("💡 If bot still fails, the issue might be in command handling or environment.")
    else:
        print("\n💡 MCP client has issues that need to be resolved.")

if __name__ == "__main__":
    asyncio.run(main())