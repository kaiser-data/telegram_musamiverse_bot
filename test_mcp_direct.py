#!/usr/bin/env python3
"""
Direct MCP server testing without Telegram - simulates bot functionality
"""
import asyncio
from masumi_client import MasumiMCPClient

async def test_mcp_functionality():
    """Test all MCP functionality that the bot would use"""
    print("🧪 Testing Masumi MCP Server Functionality")
    print("=" * 50)
    
    client = MasumiMCPClient()
    
    try:
        # Test 1: List agents
        print("\n1️⃣ Testing list_agents...")
        result = await client.list_agents()
        print(f"Result: {result[:200]}..." if len(result) > 200 else f"Result: {result}")
        
        # Test 2: Query registry
        print("\n2️⃣ Testing query_registry...")
        result = await client.query_registry()
        print(f"Result: {result[:200]}..." if len(result) > 200 else f"Result: {result}")
        
        # Test 3: Query payments
        print("\n3️⃣ Testing query_payments...")
        result = await client.query_payments()
        print(f"Result: {result[:200]}..." if len(result) > 200 else f"Result: {result}")
        
        # Test 4: Test agent schema (will fail with connection error - expected)
        print("\n4️⃣ Testing get_agent_input_schema...")
        result = await client.get_agent_input_schema("test-agent", "https://example.com/")
        print(f"Result: {result[:200]}..." if len(result) > 200 else f"Result: {result}")
        
        # Test 5: Test agent registration
        print("\n5️⃣ Testing register_agent...")
        result = await client.register_agent(
            network="Preprod",
            name="masumi-test-direct-test-001",
            api_base_url="https://test-direct.masumi-test.network/",
            selling_wallet_vkey="vkey_test_direct_123456789abcdef123456789abcdef12345678",
            capability_name="Direct Testing",
            capability_version="1.0.0",
            base_price=1000000,
            tags=["testing", "direct", "demo"],
            description="Test agent for direct MCP testing"
        )
        print(f"Result: {result[:200]}..." if len(result) > 200 else f"Result: {result}")
        
        print("\n✅ MCP Server Testing Complete!")
        print("🔍 Check results above - should show configuration errors (expected)")
        print("📝 This simulates exactly what the Telegram bot would do")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
    finally:
        await client.stop_server()

if __name__ == "__main__":
    asyncio.run(test_mcp_functionality())