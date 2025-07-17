# Development Guide

## Code Structure Analysis

### Import Dependencies

The main application uses the following imports:

```python
from telegram.ext import Updater, CommandHandler
import os  # Used for environment variable access
```

### Missing Import Fix

**Issue**: The current `main.py` has a missing import for `os` at the top level.

**Current Code**:
```python
from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text("✅ Бот на Updater работает!")

def main():
    updater = Updater(token=os.environ.get("BOT_TOKEN"), use_context=True)
    # ... rest of the code

if __name__ == "__main__":
    import os  # This should be moved to the top
    main()
```

**Recommended Fix**:
```python
import os
from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text("✅ Бот на Updater работает!")

def main():
    updater = Updater(token=os.environ.get("BOT_TOKEN"), use_context=True)
    # ... rest of the code

if __name__ == "__main__":
    main()
```

## Function-Level Documentation

### Handler Functions

#### `start(update, context)` - Command Handler

**Type**: Command Handler Function  
**Trigger**: When user sends `/start` command  
**Thread Safety**: Yes (each update handled in separate context)

**Detailed Parameters**:

1. **`update`** (`telegram.Update`):
   - `update.message`: The message object
   - `update.message.chat`: Chat information
   - `update.message.from_user`: User information
   - `update.effective_user`: Alias for from_user
   - `update.effective_chat`: Alias for chat

2. **`context`** (`telegram.ext.CallbackContext`):
   - `context.bot`: Bot instance for API calls
   - `context.args`: List of arguments passed with command
   - `context.user_data`: Persistent user-specific data storage
   - `context.chat_data`: Persistent chat-specific data storage

**Internal Flow**:
```
User sends "/start" → Telegram API → python-telegram-bot → start() → reply_text() → Telegram API → User receives response
```

**Error Handling**: Currently none implemented. Consider adding:
```python
def start(update, context):
    try:
        update.message.reply_text("✅ Бот на Updater работает!")
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        update.message.reply_text("An error occurred. Please try again.")
```

### Application Functions

#### `main()` - Application Entry Point

**Type**: Application Bootstrap Function  
**Execution**: Single-threaded main loop  
**Lifecycle**: Runs until interrupted (Ctrl+C) or system signal

**Detailed Flow**:

1. **Initialization Phase**:
   ```python
   updater = Updater(token=os.environ.get("BOT_TOKEN"), use_context=True)
   ```
   - Validates BOT_TOKEN
   - Creates HTTP client for Telegram API
   - Initializes dispatcher for handling updates

2. **Handler Registration Phase**:
   ```python
   dp = updater.dispatcher
   dp.add_handler(CommandHandler("start", start))
   ```
   - Gets dispatcher instance
   - Registers command handlers
   - Sets up routing for incoming messages

3. **Runtime Phase**:
   ```python
   updater.start_polling()
   updater.idle()
   ```
   - Starts polling loop (long-polling HTTP requests)
   - Enters idle state (waits for interruption signals)

**Configuration Options**:
```python
# Enhanced main() with configuration
def main():
    # Error handling for missing token
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable is required")
    
    # Updater with custom configuration
    updater = Updater(
        token=token,
        use_context=True,
        request_kwargs={
            'read_timeout': 6,
            'connect_timeout': 7
        }
    )
    
    dp = updater.dispatcher
    
    # Add error handler
    dp.add_error_handler(error_handler)
    
    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    
    # Start with webhook support
    if os.environ.get("USE_WEBHOOK"):
        updater.start_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 8443)),
            url_path=token,
            webhook_url=f"{os.environ.get('WEBHOOK_URL')}/{token}"
        )
    else:
        updater.start_polling()
    
    updater.idle()
```

## Advanced Usage Examples

### Enhanced Command Handlers

#### Command with Arguments
```python
def echo(update, context):
    """
    Echo command that repeats user input
    Usage: /echo <text>
    """
    if not context.args:
        update.message.reply_text("Usage: /echo <text>")
        return
    
    text = " ".join(context.args)
    update.message.reply_text(f"You said: {text}")

# Register: dp.add_handler(CommandHandler("echo", echo))
```

#### Inline Keyboard Example
```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def menu(update, context):
    """
    Display inline keyboard menu
    """
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data='1')],
        [InlineKeyboardButton("Option 2", callback_data='2')],
        [InlineKeyboardButton("Cancel", callback_data='cancel')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose an option:', reply_markup=reply_markup)

def button_handler(update, context):
    """
    Handle inline keyboard button presses
    """
    query = update.callback_query
    query.answer()  # Acknowledge the callback
    
    if query.data == '1':
        query.edit_message_text("You chose Option 1")
    elif query.data == '2':
        query.edit_message_text("You chose Option 2")
    elif query.data == 'cancel':
        query.edit_message_text("Cancelled")

# Register handlers:
# dp.add_handler(CommandHandler("menu", menu))
# dp.add_handler(CallbackQueryHandler(button_handler))
```

### Message Handlers

#### Text Message Handler
```python
from telegram.ext import MessageHandler, Filters

def handle_text(update, context):
    """
    Handle all text messages that are not commands
    """
    user_message = update.message.text
    response = f"You sent: {user_message}"
    update.message.reply_text(response)

# Register: dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
```

#### File Upload Handler
```python
def handle_document(update, context):
    """
    Handle document uploads
    """
    document = update.message.document
    file_name = document.file_name
    file_size = document.file_size
    
    # Download file (be cautious with file sizes)
    if file_size < 1024 * 1024:  # 1MB limit
        file = context.bot.get_file(document.file_id)
        file.download(f"downloads/{file_name}")
        update.message.reply_text(f"Downloaded: {file_name}")
    else:
        update.message.reply_text("File too large!")

# Register: dp.add_handler(MessageHandler(Filters.document, handle_document))
```

## Error Handling Patterns

### Global Error Handler
```python
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def error_handler(update, context):
    """
    Global error handler for all unhandled exceptions
    """
    logger.warning(f'Update {update} caused error {context.error}')
    
    if update and update.effective_message:
        update.effective_message.reply_text(
            "Sorry, an error occurred while processing your request."
        )

# Register: dp.add_error_handler(error_handler)
```

### Specific Error Handling
```python
from telegram.error import BadRequest, TimedOut, NetworkError

def robust_start(update, context):
    try:
        update.message.reply_text("✅ Бот на Updater работает!")
    except BadRequest as e:
        logger.error(f"Bad request: {e}")
    except TimedOut as e:
        logger.error(f"Request timed out: {e}")
    except NetworkError as e:
        logger.error(f"Network error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        # Optionally notify admin
```

## Testing Framework

### Unit Tests with Mocking
```python
import unittest
from unittest.mock import Mock, patch
from main import start, main

class TestBotHandlers(unittest.TestCase):
    
    def setUp(self):
        self.update = Mock()
        self.context = Mock()
    
    def test_start_command_success(self):
        """Test successful start command execution"""
        start(self.update, self.context)
        
        self.update.message.reply_text.assert_called_once_with(
            "✅ Бот на Updater работает!"
        )
    
    def test_start_command_with_exception(self):
        """Test start command when reply_text raises exception"""
        self.update.message.reply_text.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception):
            start(self.update, self.context)
    
    @patch('main.os.environ.get')
    @patch('main.Updater')
    def test_main_with_valid_token(self, mock_updater, mock_env):
        """Test main function with valid bot token"""
        mock_env.return_value = "valid_token"
        mock_updater_instance = Mock()
        mock_updater.return_value = mock_updater_instance
        
        # This would need to be adapted based on how you handle the infinite loop
        # main()  # Would run indefinitely
        
        mock_updater.assert_called_once()
        mock_updater_instance.start_polling.assert_called_once()

if __name__ == '__main__':
    unittest.main()
```

### Integration Tests
```python
import pytest
from telegram import Update, Message, User, Chat
from telegram.ext import CallbackContext

def create_mock_update(text="/start", user_id=123, chat_id=123):
    """Helper function to create mock updates for testing"""
    user = User(id=user_id, first_name="Test", is_bot=False)
    chat = Chat(id=chat_id, type="private")
    message = Message(
        message_id=1,
        date=None,
        chat=chat,
        from_user=user,
        text=text
    )
    return Update(update_id=1, message=message)

def test_start_integration():
    """Integration test for start command"""
    update = create_mock_update("/start")
    context = CallbackContext.from_update(update, None)
    
    # Mock the reply_text method
    update.message.reply_text = Mock()
    
    start(update, context)
    
    update.message.reply_text.assert_called_with("✅ Бот на Updater работает!")
```

## Performance Optimization

### Memory Management
```python
import gc
import psutil

def monitor_memory():
    """Monitor memory usage"""
    process = psutil.Process()
    memory_info = process.memory_info()
    return {
        'rss': memory_info.rss / 1024 / 1024,  # MB
        'vms': memory_info.vms / 1024 / 1024   # MB
    }

def cleanup_handler(update, context):
    """Periodic cleanup handler"""
    gc.collect()
    memory = monitor_memory()
    logger.info(f"Memory usage: RSS={memory['rss']:.2f}MB, VMS={memory['vms']:.2f}MB")
```

### Rate Limiting
```python
from functools import wraps
from time import time

def rate_limit(max_calls=10, period=60):
    """Rate limiting decorator"""
    def decorator(func):
        calls = {}
        
        @wraps(func)
        def wrapper(update, context):
            user_id = update.effective_user.id
            now = time()
            
            if user_id not in calls:
                calls[user_id] = []
            
            # Remove old calls
            calls[user_id] = [call for call in calls[user_id] if now - call < period]
            
            if len(calls[user_id]) >= max_calls:
                update.message.reply_text("Rate limit exceeded. Please try again later.")
                return
            
            calls[user_id].append(now)
            return func(update, context)
        
        return wrapper
    return decorator

@rate_limit(max_calls=5, period=60)
def limited_start(update, context):
    """Rate-limited start command"""
    update.message.reply_text("✅ Бот на Updater работает!")
```

## Security Best Practices

### Input Validation
```python
import re

def validate_command_input(text, max_length=1000):
    """Validate user input for commands"""
    if len(text) > max_length:
        return False, "Input too long"
    
    # Check for potentially malicious patterns
    dangerous_patterns = [
        r'<script.*?>',
        r'javascript:',
        r'on\w+\s*=',
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False, "Invalid input detected"
    
    return True, "Valid"

def secure_echo(update, context):
    """Secure version of echo command"""
    if not context.args:
        update.message.reply_text("Usage: /echo <text>")
        return
    
    text = " ".join(context.args)
    is_valid, message = validate_command_input(text)
    
    if not is_valid:
        update.message.reply_text(f"Error: {message}")
        return
    
    # Escape HTML characters
    escaped_text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    update.message.reply_text(f"You said: {escaped_text}")
```

### User Authorization
```python
AUTHORIZED_USERS = [123456789, 987654321]  # Admin user IDs

def admin_only(func):
    """Decorator to restrict commands to authorized users"""
    @wraps(func)
    def wrapper(update, context):
        user_id = update.effective_user.id
        if user_id not in AUTHORIZED_USERS:
            update.message.reply_text("You are not authorized to use this command.")
            return
        return func(update, context)
    return wrapper

@admin_only
def admin_command(update, context):
    """Admin-only command"""
    update.message.reply_text("Admin command executed!")
```

## Deployment Strategies

### Environment-Specific Configuration
```python
import os
from dataclasses import dataclass

@dataclass
class Config:
    bot_token: str
    webhook_url: str = None
    use_webhook: bool = False
    debug: bool = False
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls):
        return cls(
            bot_token=os.environ["BOT_TOKEN"],
            webhook_url=os.environ.get("WEBHOOK_URL"),
            use_webhook=os.environ.get("USE_WEBHOOK", "false").lower() == "true",
            debug=os.environ.get("DEBUG", "false").lower() == "true",
            log_level=os.environ.get("LOG_LEVEL", "INFO")
        )

def create_app(config: Config):
    """Application factory pattern"""
    updater = Updater(token=config.bot_token, use_context=True)
    dp = updater.dispatcher
    
    # Configure logging
    logging.basicConfig(level=getattr(logging, config.log_level))
    
    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    
    return updater
```

### Health Check Endpoint
```python
from flask import Flask, jsonify
import threading

app = Flask(__name__)
bot_status = {"status": "unknown", "last_update": None}

@app.route("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify(bot_status)

def run_health_server():
    """Run health check server in separate thread"""
    app.run(host="0.0.0.0", port=8080)

def start_health_monitor():
    """Start health monitoring"""
    health_thread = threading.Thread(target=run_health_server)
    health_thread.daemon = True
    health_thread.start()
```

This development guide provides comprehensive coverage of the codebase structure, advanced patterns, testing strategies, and production considerations for the Telegram bot application.