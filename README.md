# Telegram Bot Project

A simple Telegram bot built with Python using the `python-telegram-bot` library.

## 📋 Overview

This project implements a minimal Telegram bot that responds to user commands. Currently supports the `/start` command with a Russian language response.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your bot token:**
   ```bash
   export BOT_TOKEN="your_telegram_bot_token"
   ```

3. **Run the bot:**
   ```bash
   python main.py
   ```

## 📚 Documentation

This project includes comprehensive documentation covering all aspects of the codebase:

### 📖 Main Documentation
- **[API Documentation](./API_DOCUMENTATION.md)** - Complete guide covering all public APIs, functions, and components with examples
- **[Development Guide](./DEVELOPMENT_GUIDE.md)** - In-depth technical guide for developers with advanced patterns and best practices
- **[API Reference](./API_REFERENCE.md)** - Quick reference guide for all APIs and common patterns

### 🔧 Quick Reference

#### Available Commands
| Command | Description |
|---------|-------------|
| `/start` | Initialize bot interaction and display welcome message |

#### Core Functions
- `start(update, context)` - Handles the `/start` command
- `main()` - Application entry point and bot setup

## 📁 Project Structure

```
.
├── main.py                    # Main bot application
├── requirements.txt           # Python dependencies
├── runtime.txt               # Python runtime specification
├── README.md                 # Project overview (this file)
├── API_DOCUMENTATION.md      # Comprehensive API documentation
├── DEVELOPMENT_GUIDE.md      # Technical development guide
└── API_REFERENCE.md          # Quick reference guide
```

## 🛠 Technology Stack

- **Python 3.10.13** - Runtime environment
- **python-telegram-bot 13.15** - Telegram Bot API wrapper
- **Polling-based** - Uses long-polling for receiving updates

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `BOT_TOKEN` | Yes | Telegram Bot API token from @BotFather | `1234567890:ABCdefGH...` |

### Optional Configuration
- `WEBHOOK_URL` - For webhook-based deployment
- `USE_WEBHOOK` - Enable webhook mode (default: false)
- `DEBUG` - Enable debug mode (default: false)
- `LOG_LEVEL` - Logging level (default: INFO)

## 🚦 Getting Started

### Prerequisites
1. Python 3.10.13 or compatible version
2. Telegram account
3. Bot token from [@BotFather](https://t.me/botfather)

### Creating a Bot Token
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the provided bot token

### Local Development
```bash
# Clone the repository
git clone <repository-url>
cd telegram-bot

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export BOT_TOKEN="your_bot_token_here"

# Run the bot
python main.py
```

### Testing the Bot
1. Start the bot locally
2. Find your bot on Telegram using the username you set with @BotFather
3. Send `/start` command
4. You should receive: "✅ Бот на Updater работает!"

## 🔍 Documentation Deep Dive

### For Users
- **[API Documentation](./API_DOCUMENTATION.md)** provides complete setup instructions, command usage, troubleshooting, and deployment guides

### For Developers
- **[Development Guide](./DEVELOPMENT_GUIDE.md)** covers code structure, advanced patterns, testing frameworks, security practices, and performance optimization
- **[API Reference](./API_REFERENCE.md)** offers quick syntax references and common code patterns

### Key Documentation Sections

#### API Documentation Covers:
- Complete setup and installation guide
- All public APIs and functions with examples
- Bot commands and their responses
- Deployment strategies (local, Heroku, Docker)
- Error handling and troubleshooting
- Security considerations
- Testing approaches
- Extension points for adding features

#### Development Guide Covers:
- Detailed code structure analysis
- Function-level documentation with internal flows
- Advanced usage examples (keyboards, file handling)
- Error handling patterns
- Testing frameworks (unit and integration tests)
- Performance optimization techniques
- Security best practices
- Deployment strategies and configuration patterns

#### API Reference Covers:
- Quick command and function reference
- Object property references
- Handler patterns and examples
- Common usage patterns
- Testing quick reference

## 🧪 Testing

The project includes comprehensive testing documentation:

```bash
# Run unit tests (example)
python -m unittest test_bot.py

# Run with coverage
python -m pytest --cov=main tests/
```

See [Development Guide](./DEVELOPMENT_GUIDE.md#testing-framework) for detailed testing examples.

## 🚀 Deployment

### Local Development
```bash
export BOT_TOKEN="your_token"
python main.py
```

### Heroku
```bash
heroku config:set BOT_TOKEN="your_token"
git push heroku main
```

### Docker
```dockerfile
FROM python:3.10.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

See [API Documentation](./API_DOCUMENTATION.md#deployment) for detailed deployment instructions.

## 🔒 Security

- Keep your `BOT_TOKEN` secure and never commit it to version control
- Validate user inputs in command handlers
- Consider rate limiting for production use
- Handle user data according to privacy regulations

See [Development Guide](./DEVELOPMENT_GUIDE.md#security-best-practices) for comprehensive security guidance.

## 🐛 Troubleshooting

### Common Issues
1. **Missing BOT_TOKEN**: Ensure environment variable is set
2. **Invalid Token**: Verify token with @BotFather
3. **Network Issues**: Check internet connection and Telegram API status

See [API Documentation](./API_DOCUMENTATION.md#error-handling-and-troubleshooting) for detailed troubleshooting guide.

## 📈 Performance

- Current implementation uses polling (suitable for development)
- Consider webhooks for production deployments
- Monitor memory usage for complex implementations
- Bot handles updates sequentially by default

See [Development Guide](./DEVELOPMENT_GUIDE.md#performance-optimization) for optimization techniques.

## 🔧 Extension Examples

### Adding New Commands
```python
def hello(update, context):
    update.message.reply_text("Hello, World!")

# In main():
dp.add_handler(CommandHandler("hello", hello))
```

### Adding Message Handlers
```python
def echo(update, context):
    update.message.reply_text(update.message.text)

# In main():
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
```

See documentation files for comprehensive extension examples.

## 📄 License

[Specify your license here]

## 🤝 Contributing

1. Follow the existing code structure
2. Add appropriate error handling
3. Update documentation for new features
4. Test thoroughly before submitting
5. Maintain backward compatibility

## 📞 Support

- Check the comprehensive documentation in this repository
- Review [python-telegram-bot documentation](https://python-telegram-bot.readthedocs.io/)
- Check [Telegram Bot API documentation](https://core.telegram.org/bots/api)

## 📊 Project Status

- **Version**: 1.0
- **Status**: Active Development
- **Python**: 3.10.13
- **Dependencies**: python-telegram-bot 13.15

---

**Note**: This README provides a high-level overview. For detailed technical information, implementation examples, and advanced usage patterns, please refer to the comprehensive documentation files linked throughout this document.