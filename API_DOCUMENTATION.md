# Telegram Bot API Documentation

## Overview

This is a simple Telegram bot built using the `python-telegram-bot` library. The bot provides basic functionality with a `/start` command that responds with a confirmation message.

## Project Structure

```
.
├── main.py           # Main bot application
├── requirements.txt  # Python dependencies
├── runtime.txt      # Python runtime specification
└── README.md        # This documentation
```

## Dependencies

- **python-telegram-bot==13.15**: Telegram Bot API wrapper for Python
- **Python 3.10.13**: Runtime environment

## Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `BOT_TOKEN` | Telegram Bot API token obtained from @BotFather | Yes | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |

## Public APIs and Functions

### `start(update, context)`

**Description**: Handler function for the `/start` command. Sends a welcome message to the user.

**Parameters**:
- `update` (telegram.Update): Contains information about the incoming update
- `context` (telegram.ext.CallbackContext): Context object that contains additional information

**Returns**: None

**Side Effects**: Sends a reply message to the user

**Example Usage**:
```python
# This function is automatically called when a user sends /start
# No direct invocation needed - handled by the Telegram framework
```

**Response**: "✅ Бот на Updater работает!" (Bot on Updater is working!)

### `main()`

**Description**: Main entry point of the application. Sets up the Telegram bot, registers command handlers, and starts polling for updates.

**Parameters**: None

**Returns**: None

**Side Effects**:
- Creates an Updater instance
- Registers command handlers
- Starts the bot polling loop
- Keeps the application running until interrupted

**Example Usage**:
```python
if __name__ == "__main__":
    main()  # Starts the bot
```

## Bot Commands

### `/start`

**Description**: Initial command to interact with the bot

**Usage**: `/start`

**Response**: "✅ Бот на Updater работает!"

**Example**:
```
User: /start
Bot: ✅ Бот на Updater работает!
```

## Setup and Installation

### Prerequisites

1. Python 3.10.13 or compatible version
2. Telegram Bot Token (obtain from @BotFather on Telegram)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variable**:
   ```bash
   export BOT_TOKEN="your_bot_token_here"
   ```

4. **Run the bot**:
   ```bash
   python main.py
   ```

### Alternative Environment Variable Setup

You can also create a `.env` file (not included in repository for security):
```bash
# .env file
BOT_TOKEN=your_bot_token_here
```

Then modify the code to load from `.env`:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Deployment

### Local Development

```bash
export BOT_TOKEN="your_token"
python main.py
```

### Production Deployment

The project includes `runtime.txt` which suggests compatibility with platforms like Heroku:

1. **Heroku Deployment**:
   ```bash
   # Set environment variable in Heroku
   heroku config:set BOT_TOKEN="your_token"
   
   # Deploy
   git push heroku main
   ```

2. **Docker Deployment** (example Dockerfile):
   ```dockerfile
   FROM python:3.10.13-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "main.py"]
   ```

## Error Handling and Troubleshooting

### Common Issues

1. **Missing BOT_TOKEN**:
   - Error: Bot will fail to start
   - Solution: Ensure BOT_TOKEN environment variable is set

2. **Invalid Token**:
   - Error: `telegram.error.InvalidToken`
   - Solution: Verify token with @BotFather

3. **Network Issues**:
   - Error: Connection timeouts
   - Solution: Check internet connection and Telegram API status

### Debugging

Enable logging for detailed debugging:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## API Response Formats

### Standard Message Response

```json
{
  "message_id": 123,
  "from": {
    "id": 987654321,
    "is_bot": false,
    "first_name": "User"
  },
  "chat": {
    "id": 987654321,
    "first_name": "User",
    "type": "private"
  },
  "date": 1640995200,
  "text": "/start"
}
```

## Extension Points

### Adding New Commands

```python
def new_command(update, context):
    update.message.reply_text("New command response")

# In main() function:
dp.add_handler(CommandHandler("newcommand", new_command))
```

### Adding Message Handlers

```python
from telegram.ext import MessageHandler, Filters

def echo(update, context):
    update.message.reply_text(update.message.text)

# In main() function:
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
```

## Security Considerations

1. **Token Security**: Never commit BOT_TOKEN to version control
2. **Input Validation**: Validate user inputs in command handlers
3. **Rate Limiting**: Consider implementing rate limiting for production use
4. **User Privacy**: Handle user data according to privacy regulations

## Testing

### Manual Testing

1. Start the bot locally
2. Open Telegram and find your bot
3. Send `/start` command
4. Verify response

### Unit Testing Example

```python
import unittest
from unittest.mock import Mock
from main import start

class TestBotHandlers(unittest.TestCase):
    def test_start_command(self):
        update = Mock()
        context = Mock()
        
        start(update, context)
        
        update.message.reply_text.assert_called_once_with("✅ Бот на Updater работает!")
```

## Performance Considerations

- **Polling vs Webhooks**: Current implementation uses polling; consider webhooks for production
- **Concurrent Updates**: The bot handles updates sequentially by default
- **Memory Usage**: Minimal for this simple bot; monitor for complex implementations

## Version History

- **v1.0**: Initial implementation with basic `/start` command

## Contributing

When extending this bot:

1. Follow the existing code structure
2. Add appropriate error handling
3. Update this documentation
4. Test new features thoroughly
5. Maintain backward compatibility

## License

[Specify your license here]

## Support

For issues and questions:
- Check the [python-telegram-bot documentation](https://python-telegram-bot.readthedocs.io/)
- Review Telegram Bot API documentation
- Check common troubleshooting steps above