#!/usr/bin/env python3
"""
Quick test to debug MCP connection issues
"""
import asyncio
from masumi_client import MasumiMCPClient

async def test_connection():
    print("🧪 Testing MCP Connection with Debug Info")
    print("=" * 50)
    
    client = MasumiMCPClient()
    
    try:
        print("\n1️⃣ Testing client initialization and server startup...")
        result = await client.list_agents()
        print(f"✅ Result: {result[:100]}..." if len(result) > 100 else f"✅ Result: {result}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await client.stop_server()

if __name__ == "__main__":
    asyncio.run(test_connection())