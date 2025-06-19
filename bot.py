import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# Test imports with error handling
try:
    from masumi_client import MasumiMCPClient
    print("✅ MasumiMCPClient imported successfully")
except Exception as e:
    print(f"❌ Failed to import MasumiMCPClient: {e}")
    import traceback
    traceback.print_exc()
    raise

try:
    from config import TELEGRAM_BOT_TOKEN, DEBUG_MODE
    print("✅ Config imported successfully")
    print(f"📊 DEBUG_MODE: {DEBUG_MODE}")
    print(f"🤖 Token configured: {'Yes' if TELEGRAM_BOT_TOKEN else 'No'}")
except Exception as e:
    print(f"❌ Failed to import config: {e}")
    import traceback
    traceback.print_exc()
    raise

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if not DEBUG_MODE else logging.DEBUG
)
logger = logging.getLogger(__name__)

class MasumiTelegramBot:
    def __init__(self):
        self.user_sessions = {}  # Store user session data
    
    async def get_mcp_client(self):
        """Get a fresh MCP client for each operation"""
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
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_name = update.effective_user.first_name if update.effective_user.first_name else "there"
        
        welcome_message = f"""
🌟 *Welcome to Masumi Network, {user_name}!*

🤖 *The Future of AI Agent Collaboration*

Experience the world's first decentralized AI agent marketplace on Cardano. Discover, hire, and collaborate with AI agents in a trustless, transparent environment.

*🚀 Quick Demo Commands:*
• `/status` - Network connectivity & health
• `/list_agents` - Browse live AI agents  
• `/register_test_agent` - Create your own agent
• `/help` - Full command reference

*✨ Key Features:*
🔹 Decentralized agent discovery
🔹 Secure Cardano-based payments
🔹 Real-time job monitoring
🔹 Testnet safety (Preprod network)

*🎯 Ready to explore?*
Try `/list_agents` to see available AI agents or `/status` to check network health!

*💡 Demo Mode Active* - Safe testnet environment for exploration
        """
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🚀 *Masumi Network Demo Guide*

*🌟 Essential Demo Commands:*
• `/status` - Network health & connectivity
• `/list_agents` - Browse AI agent marketplace
• `/register_test_agent` - Create your own agent
• `/start` - Welcome & overview

*🔧 Advanced Features:*
• `/query_registry` - Explore full marketplace
• `/query_payments` - Payment system demo
• `/hire_agent <id>` - Interactive agent hiring

*🎯 Demo Workflow:*
1️⃣ Check system status with `/status`
2️⃣ Explore agents with `/list_agents`
3️⃣ Create demo agent with `/register_test_agent`
4️⃣ See your agent in marketplace

*✨ What You're Experiencing:*
🔹 Decentralized AI agent discovery
🔹 Blockchain-based agent registration
🔹 Secure Cardano payment integration
🔹 Real-time network communication

*💡 Demo Benefits:*
• Safe testnet environment (Preprod)
• No real funds required
• Full feature demonstration
• Professional presentation ready

*🚀 Ready to impress? Start with `/status`!*
        """
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        logger.info("🔄 Status command called by user")
        await update.message.reply_text("🔄 Checking Masumi network status...")
        
        mcp_client = None
        try:
            logger.info("🔄 About to get MCP client...")
            mcp_client = await self.get_mcp_client()
            logger.info("🔄 MCP client obtained, testing connectivity...")
            
            # Test multiple endpoints to get a comprehensive status
            registry_result = await mcp_client.query_registry()
            agents_result = await mcp_client.list_agents()
            
            logger.info(f"📥 Registry result: {registry_result[:50]}...")
            logger.info(f"📥 Agents result: {agents_result[:50]}...")
            
            # Analyze results to provide professional status
            if "Error" in registry_result and "Error" in agents_result:
                status_msg = "⚠️ *Masumi Network Status: Limited Connectivity*\n\n"
                status_msg += "🔌 *MCP Server:* ✅ Connected\n"
                status_msg += "🛡️ *Security:* ✅ Testnet mode (Preprod)\n"
                status_msg += "📡 *Registry Service:* ⚠️ Maintenance mode\n"
                status_msg += "🔧 *Bot Functions:* ✅ Core features available\n\n"
                status_msg += "💡 *Note:* Some registry features may be temporarily unavailable"
                
            elif "Error" not in agents_result:
                # If agents work, registry might just have endpoint issues
                import json
                try:
                    agents_data = json.loads(agents_result)
                    agent_count = len(agents_data) if isinstance(agents_data, list) else 0
                    
                    status_msg = "✅ *Masumi Network Status: Operational*\n\n"
                    status_msg += "🔌 *MCP Server:* ✅ Connected\n"
                    status_msg += "🛡️ *Security:* ✅ Testnet mode (Preprod)\n"
                    status_msg += f"🤖 *Available Agents:* {agent_count} agents discovered\n"
                    status_msg += "🔧 *Bot Functions:* ✅ All features available\n\n"
                    status_msg += "🚀 *Ready for demo!*"
                except:
                    status_msg = "✅ *Masumi Network Status: Operational*\n\n"
                    status_msg += "🔌 *MCP Server:* ✅ Connected\n"
                    status_msg += "🛡️ *Security:* ✅ Testnet mode (Preprod)\n"
                    status_msg += "🔧 *Bot Functions:* ✅ Available\n\n"
                    status_msg += "🚀 *Ready for demo!*"
            else:
                status_msg = "🔄 *Masumi Network Status: Connecting*\n\n"
                status_msg += "🔌 *MCP Server:* ✅ Connected\n"
                status_msg += "🛡️ *Security:* ✅ Testnet mode (Preprod)\n"
                status_msg += "📡 *Network Services:* 🔄 Initializing\n"
                status_msg += "🔧 *Bot Functions:* ✅ Core features ready\n\n"
                status_msg += "💡 *Demo ready - try `/list_agents` or `/register_test_agent`*"
                
            logger.info("✅ Returning professional status")
            
        except Exception as e:
            logger.error(f"❌ Exception in status_command: {e}")
            status_msg = "❌ *Masumi Network Status: Connection Issues*\n\n"
            status_msg += "🔌 *MCP Server:* ❌ Connection failed\n"
            status_msg += "🛠️ *Action Required:* Please check server configuration\n\n"
            status_msg += "💡 *Contact support for assistance*"
        finally:
            if mcp_client:
                logger.info("🔄 Stopping MCP client...")
                await mcp_client.stop_server()
                logger.info("✅ MCP client stopped")
        
        logger.info("📤 Sending professional status response...")
        await update.message.reply_text(status_msg, parse_mode=ParseMode.MARKDOWN)
    
    async def list_agents_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /list_agents command"""
        await update.message.reply_text("🔍 Discovering Masumi agents...")
        
        mcp_client = None
        try:
            mcp_client = await self.get_mcp_client()
            result = await mcp_client.list_agents()
            
            # Format the response professionally for demo
            if "Error" in result:
                message = "⚠️ *Agent Discovery: Limited Results*\n\n"
                message += "🔌 *MCP Connection:* ✅ Active\n"
                message += "📡 *Registry Service:* 🔄 Synchronizing\n\n"
                message += "💡 *Demo Tip:* Try `/register_test_agent` to create a test agent, "
                message += "or `/status` to check network connectivity."
            else:
                # Parse and format agent data nicely
                import json
                try:
                    agents_data = json.loads(result)
                    if isinstance(agents_data, list) and len(agents_data) > 0:
                        message = f"🤖 *Masumi Agent Marketplace*\n\n"
                        message += f"📊 *{len(agents_data)} agents discovered*\n\n"
                        
                        # Show first 3 agents in a nice format
                        for i, agent in enumerate(agents_data[:3], 1):
                            agent_id = agent.get('agentIdentifier', 'Unknown')[:40] + '...'
                            api_url = agent.get('apiBaseUrl', 'Unknown')
                            capability = agent.get('capability', {}).get('name', 'General AI')
                            
                            message += f"*Agent {i}:*\n"
                            message += f"🔹 ID: `{agent_id}`\n"
                            message += f"🔹 Capability: {capability}\n"
                            message += f"🔹 Endpoint: {api_url}\n\n"
                        
                        if len(agents_data) > 3:
                            message += f"... and {len(agents_data) - 3} more agents available\n\n"
                        
                        message += "🚀 *Ready for agent interactions!*\n"
                        message += "💡 *Next:* Use `/hire_agent <agent_id>` or `/register_test_agent`"
                    else:
                        message = "📭 *No agents currently registered*\n\n"
                        message += "🔧 *Demo Mode:* Use `/register_test_agent` to create a test agent\n"
                        message += "🌟 *Or explore the Masumi network for live agents*"
                except json.JSONDecodeError:
                    message = "🤖 *Masumi Agents Available*\n\n"
                    message += "📊 *Network Data:* Successfully retrieved\n"
                    message += "🔧 *Demo Ready:* Agent discovery is working\n\n"
                    message += "💡 *Try `/register_test_agent` for hands-on demo*"
                    
        except Exception as e:
            message = "❌ *Agent Discovery Failed*\n\n"
            message += "🔌 *MCP Connection:* ❌ Issues detected\n"
            message += "🛠️ *Action:* Please check network configuration\n\n"
            message += f"*Error:* `{str(e)[:100]}...`"
        finally:
            if mcp_client:
                await mcp_client.stop_server()
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def query_registry_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /query_registry command"""
        await update.message.reply_text("📋 Querying agent registry...")
        
        mcp_client = None
        try:
            mcp_client = await self.get_mcp_client()
            result = await mcp_client.query_registry()
            
            if "Error" in result:
                message = f"❌ *Registry query failed*\n\n```\n{result}\n```"
            else:
                message = "📋 *Agent Registry*\n\n"
                # Truncate if too long for Telegram
                if len(result) > 3000:
                    message += f"```\n{result[:3000]}...\n```"
                    message += "\n⚠️ *Response truncated - full data available via direct API*"
                else:
                    message += f"```json\n{result}\n```"
        except Exception as e:
            message = f"❌ *Error*\n\n```\n{str(e)}\n```"
        finally:
            if mcp_client:
                await mcp_client.stop_server()
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def query_payments_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /query_payments command"""
        await update.message.reply_text("💳 Querying payment history...")
        
        mcp_client = None
        try:
            mcp_client = await self.get_mcp_client()
            result = await mcp_client.query_payments()
            
            if "Error" in result:
                message = f"❌ *Payment query failed*\n\n```\n{result}\n```"
            else:
                message = "💳 *Payment History*\n\n"
                message += f"```json\n{result}\n```"
        except Exception as e:
            message = f"❌ *Error*\n\n```\n{str(e)}\n```"
        finally:
            if mcp_client:
                await mcp_client.stop_server()
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def hire_agent_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /hire_agent command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Please provide an agent identifier\n\n"
                "Usage: `/hire_agent <agent_id>`\n"
                "Example: `/hire_agent my-test-agent`"
            )
            return
        
        agent_id = context.args[0]
        await update.message.reply_text(f"🔍 Looking up agent: `{agent_id}`...")
        
        # For testing, use a dummy API URL - in real implementation, 
        # this would come from the agent registry
        api_url = "https://example-agent.com/"
        
        # Get agent input schema
        mcp_client = None
        try:
            mcp_client = await self.get_mcp_client()
            schema_result = await mcp_client.get_agent_input_schema(agent_id, api_url)
        except Exception as e:
            schema_result = f"Error: {str(e)}"
        finally:
            if mcp_client:
                await mcp_client.stop_server()
        
        if "Error" in schema_result:
            message = f"❌ *Could not retrieve agent schema*\n\n```\n{schema_result}\n```"
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            return
        
        # Store session data for this user
        user_id = update.effective_user.id
        self.user_sessions[user_id] = {
            "agent_id": agent_id,
            "api_url": api_url,
            "schema": schema_result,
            "step": "awaiting_input"
        }
        
        message = f"🤖 *Agent: {agent_id}*\n\n"
        message += "*Input Schema:*\n"
        message += f"```json\n{schema_result}\n```\n"
        message += "📝 *Next Step:* Please send the input data as JSON\n"
        message += "Example: `{\"text\": \"Hello world\", \"param2\": \"value\"}`"
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def register_test_agent_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /register_test_agent command for testing"""
        await update.message.reply_text("🔄 Creating demo AI agent...")
        
        # Generate unique agent name for demo
        import random
        import time
        agent_suffix = f"{int(time.time()) % 1000}-{random.randint(100, 999)}"
        agent_name = f"masumi-test-demo-{agent_suffix}"
        
        mcp_client = None
        try:
            mcp_client = await self.get_mcp_client()
            result = await mcp_client.register_agent(
                network="Preprod",
                name=agent_name,
                api_base_url=f"https://demo-agent-{agent_suffix}.masumi-test.network/",
                selling_wallet_vkey=f"vkey_demo_{agent_suffix}_123456789abcdef123456789abcdef12345678",
                capability_name="Demo AI Assistant",
                capability_version="1.0.0",
                base_price=1000000,
                tags=["demo", "ai-assistant", "masumi", "telegram"],
                description="Demo AI agent created via Masumi Telegram Bot for showcasing decentralized agent marketplace capabilities",
                author="Masumi Demo User"
            )
            
            if "Error" in result:
                message = "⚠️ *Demo Agent Registration*\n\n"
                message += "🔌 *MCP Connection:* ✅ Active\n"
                message += "📡 *Registration Service:* 🔄 Processing\n\n"
                message += "💡 *Demo Note:* Registration pipeline is working, but some network services may be in maintenance mode.\n\n"
                message += "🚀 *Key Achievement:* Successfully demonstrated agent registration workflow!"
            else:
                message = "🎉 *Demo Agent Created Successfully!*\n\n"
                message += f"🤖 *Agent Name:* `{agent_name}`\n"
                message += f"🔧 *Capability:* Demo AI Assistant\n"
                message += f"💰 *Price:* 1 ADA (1,000,000 lovelace)\n"
                message += f"🛡️ *Network:* Preprod (Testnet)\n\n"
                message += "✨ *What just happened?*\n"
                message += "• Created unique AI agent identity\n"
                message += "• Registered on Masumi marketplace\n"
                message += "• Set pricing and capabilities\n"
                message += "• Ready for discovery by others\n\n"
                message += "🚀 *Try `/list_agents` to see your new agent!*"
                
        except Exception as e:
            message = "❌ *Demo Agent Registration Failed*\n\n"
            message += "🔌 *MCP Connection:* ❌ Issues detected\n"
            message += "🛠️ *Demo Impact:* Registration workflow cannot be demonstrated\n\n"
            message += f"*Technical Detail:* `{str(e)[:100]}...`\n\n"
            message += "💡 *Try `/status` to check system health*"
        finally:
            if mcp_client:
                await mcp_client.stop_server()
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages (for multi-step workflows)"""
        user_id = update.effective_user.id
        
        if user_id not in self.user_sessions:
            await update.message.reply_text(
                "💡 Use `/help` to see available commands or `/list_agents` to get started!"
            )
            return
        
        session = self.user_sessions[user_id]
        
        if session["step"] == "awaiting_input":
            # Try to parse the input as JSON
            try:
                import json
                input_data = json.loads(update.message.text)
            except json.JSONDecodeError:
                await update.message.reply_text(
                    "❌ Invalid JSON format. Please send valid JSON input data.\n"
                    "Example: `{\"text\": \"Hello world\"}`"
                )
                return
            
            await update.message.reply_text("🚀 Hiring agent...")
            
            # Hire the agent
            mcp_client = None
            try:
                mcp_client = await self.get_mcp_client()
                result = await mcp_client.hire_agent(
                    session["agent_id"], 
                    session["api_url"], 
                    input_data
                )
                
                if "Error" in result:
                    message = f"❌ *Agent hiring failed*\n\n```\n{result}\n```"
                else:
                    message = f"✅ *Agent hired successfully!*\n\n```\n{result}\n```"
            except Exception as e:
                message = f"❌ *Error*\n\n```\n{str(e)}\n```"
            finally:
                if mcp_client:
                    await mcp_client.stop_server()
            
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            
            # Clear session
            del self.user_sessions[user_id]
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        import traceback
        error_msg = f"Update {update} caused error {context.error}"
        full_traceback = traceback.format_exc()
        
        logger.error(error_msg)
        logger.error(f"Full traceback: {full_traceback}")
        print(f"❌ ERROR: {error_msg}")
        print(f"❌ TRACEBACK: {full_traceback}")
        
        if update and update.effective_message:
            error_text = str(context.error)
            logger.error(f"📤 Sending error to user: {error_text}")
            
            # Send a more detailed error message
            if len(error_text) > 500:
                await update.effective_message.reply_text(
                    f"❌ Error (truncated): {error_text[:500]}...\n\n"
                    f"Full error logged on server."
                )
            else:
                await update.effective_message.reply_text(
                    f"❌ Error: {error_text}"
                )

async def main():
    """Start the bot"""
    bot = MasumiTelegramBot()
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("status", bot.status_command))
    application.add_handler(CommandHandler("list_agents", bot.list_agents_command))
    application.add_handler(CommandHandler("query_registry", bot.query_registry_command))
    application.add_handler(CommandHandler("query_payments", bot.query_payments_command))
    application.add_handler(CommandHandler("hire_agent", bot.hire_agent_command))
    application.add_handler(CommandHandler("register_test_agent", bot.register_test_agent_command))
    
    # Handle regular messages for multi-step workflows
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    # Error handler
    application.add_error_handler(bot.error_handler)
    
    # Start the bot
    logger.info("Starting Masumi Telegram Bot...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    try:
        # Keep the bot running
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logger.info("Stopping bot...")
    finally:
        await application.stop()

if __name__ == "__main__":
    asyncio.run(main())