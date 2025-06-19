import asyncio
import json
import sys
import os
from typing import Dict, Any, Optional
from config import MCP_SERVER_PATH, PYTHONPATH

class MasumiMCPClient:
    """Simple MCP client for communicating with Masumi MCP server"""
    
    def __init__(self):
        self.server_process = None
        self.request_id = 1
    
    async def start_server(self):
        """Start the MCP server process"""
        if self.server_process:
            return
        
        print(f"🔄 Starting MCP server: {MCP_SERVER_PATH}")
        print(f"📁 PYTHONPATH: {PYTHONPATH}")
            
        # Create environment with current env + all required MCP server vars
        env = os.environ.copy()
        env["PYTHONPATH"] = PYTHONPATH
        
        # Load .env variables for MCP server
        from dotenv import load_dotenv
        load_dotenv()
        
        # Pass required MCP server environment variables
        mcp_env_vars = [
            "MASUMI_REGISTRY_TOKEN",
            "MASUMI_PAYMENT_TOKEN", 
            "MASUMI_NETWORK",
            "MASUMI_REGISTRY_BASE_URL",
            "MASUMI_PAYMENT_BASE_URL"
        ]
        
        for var in mcp_env_vars:
            if var in os.environ:
                env[var] = os.environ[var]
        
        try:
            # Use the system Python that has MCP dependencies, not the venv Python
            system_python = "/Users/marty/miniforge3/bin/python"
            print(f"🚀 Command: {system_python} {MCP_SERVER_PATH} stdio")
            print(f"🌍 Environment vars: {[k for k in env.keys() if 'MASUMI' in k]}")
            
            self.server_process = await asyncio.create_subprocess_exec(
                system_python, MCP_SERVER_PATH, "stdio",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
                cwd=os.path.dirname(MCP_SERVER_PATH)
            )
            print("✅ MCP server process created")
            
            # Give the server a moment to start
            await asyncio.sleep(0.5)
            
            # Check if process is still alive
            if self.server_process.returncode is not None:
                stderr_data = await self.server_process.stderr.read()
                stderr_output = stderr_data.decode()
                raise Exception(f"MCP server died immediately. Exit code: {self.server_process.returncode}. Stderr: {stderr_output}")
            
        except Exception as e:
            print(f"❌ Failed to create MCP server process: {e}")
            raise
        
        # Initialize the server
        print("🔄 Sending initialize request...")
        init_response = await self._send_request({
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "telegram-bot", "version": "1.0.0"}
            }
        })
        print(f"📨 Initialize response: {init_response}")
        
        # Send initialized notification
        print("🔄 Sending initialized notification...")
        notify_response = await self._send_request({
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        })
        print(f"📨 Notification response: {notify_response}")
        print("✅ MCP server initialized successfully")
    
    async def stop_server(self):
        """Stop the MCP server process"""
        if self.server_process:
            self.server_process.terminate()
            await self.server_process.wait()
            self.server_process = None
    
    def _next_id(self) -> int:
        """Generate next request ID"""
        self.request_id += 1
        return self.request_id
    
    async def _send_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send JSON-RPC request to server"""
        if not self.server_process:
            await self.start_server()
        
        request_json = json.dumps(request) + "\n"
        self.server_process.stdin.write(request_json.encode())
        await self.server_process.stdin.drain()
        
        try:
            response_line = await asyncio.wait_for(
                self.server_process.stdout.readline(),
                timeout=5.0
            )
            if response_line:
                return json.loads(response_line.decode())
        except asyncio.TimeoutError:
            return {"error": "Request timeout"}
        return None
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool and return formatted response"""
        try:
            # Check if server process is still alive
            if self.server_process and self.server_process.returncode is not None:
                # Server died, capture stderr for debugging
                stderr_output = ""
                if self.server_process.stderr:
                    try:
                        stderr_data = await self.server_process.stderr.read()
                        stderr_output = stderr_data.decode()
                    except:
                        pass
                return f"❌ MCP server process died. Exit code: {self.server_process.returncode}. Stderr: {stderr_output[:200]}"
            
            response = await self._send_request({
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            })
            
            if not response:
                return "❌ No response from server"
            
            if "error" in response:
                return f"❌ Error: {response['error']}"
            
            if "result" in response:
                result = response["result"]
                if "content" in result and result["content"]:
                    return result["content"][0].get("text", "No content")
            
            return "❌ Unexpected response format"
            
        except Exception as e:
            return f"❌ Connection error: {str(e)}"
    
    # Convenient wrapper methods for each tool
    async def list_agents(self) -> str:
        """List available agents"""
        return await self.call_tool("list_agents", {})
    
    async def get_agent_input_schema(self, agent_identifier: str, api_base_url: str) -> str:
        """Get agent input schema"""
        return await self.call_tool("get_agent_input_schema", {
            "agent_identifier": agent_identifier,
            "api_base_url": api_base_url
        })
    
    async def hire_agent(self, agent_identifier: str, api_base_url: str, input_data: Dict[str, Any]) -> str:
        """Hire an agent"""
        return await self.call_tool("hire_agent", {
            "agent_identifier": agent_identifier,
            "api_base_url": api_base_url,
            "input_data": input_data
        })
    
    async def check_job_status(self, agent_identifier: str, api_base_url: str, job_id: str) -> str:
        """Check job status"""
        return await self.call_tool("check_job_status", {
            "agent_identifier": agent_identifier,
            "api_base_url": api_base_url,
            "job_id": job_id
        })
    
    async def get_job_full_result(self, agent_identifier: str, api_base_url: str, job_id: str) -> str:
        """Get full job result"""
        return await self.call_tool("get_job_full_result", {
            "agent_identifier": agent_identifier,
            "api_base_url": api_base_url,
            "job_id": job_id
        })
    
    async def query_payments(self, network: str = "Preprod", limit: int = 10) -> str:
        """Query payments"""
        return await self.call_tool("query_payments", {
            "network": network,
            "limit": limit
        })
    
    async def query_registry(self, network: str = "Preprod") -> str:
        """Query registry"""
        return await self.call_tool("query_registry", {
            "network": network
        })
    
    async def register_agent(self, network: str, name: str, api_base_url: str, 
                           selling_wallet_vkey: str, capability_name: str, 
                           capability_version: str, base_price: int, **kwargs) -> str:
        """Register an agent"""
        args = {
            "network": network,
            "name": name,
            "api_base_url": api_base_url,
            "selling_wallet_vkey": selling_wallet_vkey,
            "capability_name": capability_name,
            "capability_version": capability_version,
            "base_price": base_price
        }
        args.update(kwargs)
        return await self.call_tool("register_agent", args)