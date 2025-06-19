# Masumi Telegram Bot

A Telegram bot for testing the Masumi MCP Server - provides a user-friendly interface to interact with the Masumi decentralized AI agent marketplace.

## Features

- 🤖 **Agent Discovery**: Browse and search available agents
- 💼 **Agent Hiring**: Interactive workflow to hire agents with job monitoring
- 💳 **Payment Tracking**: Query payment history and status
- 📋 **Registry Management**: View and manage agent registry
- 🛡️ **Testnet Safety**: All operations restricted to Preprod network

## Quick Setup

### 1. Install Dependencies

```bash
cd telegram-masumi-bot
pip install -r requirements.txt
```

### 2. Get Telegram Bot Token

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the bot token

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your bot token
```

### 4. Start the Bot

```bash
# Make sure the Masumi MCP server is available
python bot.py
```

## Bot Commands

### Basic Commands
- `/start` - Welcome message and bot overview
- `/help` - List all available commands
- `/status` - Check bot and MCP server status

### Agent Operations
- `/list_agents` - Browse available agents
- `/query_registry` - View full agent registry
- `/hire_agent <agent_id>` - Start interactive hiring process

### Payment Operations
- `/query_payments` - View payment history
- `/register_test_agent` - Register a test agent for testing

## Usage Workflow

1. **Start the bot**: `/start`
2. **Check status**: `/status` (verify MCP server connection)
3. **Browse agents**: `/list_agents`
4. **Hire an agent**: `/hire_agent <agent_id>`
5. **Follow prompts**: Send JSON input data when requested
6. **Monitor progress**: Bot will show job status updates

## Example Session

```
User: /start
Bot: Welcome to Masumi MCP Test Bot! ...

User: /list_agents
Bot: 🤖 Available Masumi Agents
     [Agent list in JSON format]

User: /hire_agent test-agent-001
Bot: 🤖 Agent: test-agent-001
     Input Schema: {...}
     📝 Next Step: Please send input data as JSON

User: {"text": "Hello world", "task": "greeting"}
Bot: ✅ Agent hired successfully!
     [Job details and status]
```

## Testing Mode

- **Testnet Only**: All operations use Preprod network
- **No Production Error Handling**: Basic error messages for quick testing
- **Test Data**: Agents must use `masumi-test-` prefix
- **Local MCP Server**: Connects to local Masumi MCP server instance

## Requirements

- Python 3.11+
- Running Masumi MCP Server
- Telegram bot token
- Internet connection for Telegram API

## Troubleshooting

### Bot Not Responding
- Check if bot token is correct in `.env`
- Verify MCP server is running: `/status`
- Check logs for error messages

### MCP Connection Issues
- Ensure `MCP_SERVER_PATH` points to correct server.py
- Verify `PYTHONPATH` includes server dependencies
- Check if required environment variables are set in MCP server

### Agent Operations Failing
- Verify testnet configuration (Preprod network)
- Check if agent names have `masumi-test-` prefix
- Ensure MCP server has required tokens configured# telegram_musamiverse_bot
