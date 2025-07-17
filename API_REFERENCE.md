# API Quick Reference Guide

## Command Reference

### Available Commands

| Command | Description | Usage | Response |
|---------|-------------|-------|----------|
| `/start` | Initialize bot interaction | `/start` | "✅ Бот на Updater работает!" |

## Function Reference

### Core Functions

#### `start(update, context)`
```python
def start(update, context):
    """Handler for /start command"""
    update.message.reply_text("✅ Бот на Updater работает!")
```

**Quick Usage:**
- **Trigger**: User sends `/start`
- **Parameters**: `update` (Update object), `context` (CallbackContext)
- **Returns**: None
- **Side Effect**: Sends reply message

#### `main()`
```python
def main():
    """Main application entry point"""
    updater = Updater(token=os.environ.get("BOT_TOKEN"), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()
```

**Quick Usage:**
- **Purpose**: Bootstrap and run the bot
- **Environment**: Requires `BOT_TOKEN` environment variable
- **Execution**: Runs indefinitely until interrupted

## Update Object Properties

### `update.message`
```python
update.message.text          # Message text content
update.message.chat          # Chat information
update.message.from_user     # User who sent message
update.message.message_id    # Unique message identifier
update.message.date          # Message timestamp
```

### `update.effective_*` (Aliases)
```python
update.effective_user        # Same as update.message.from_user
update.effective_chat        # Same as update.message.chat
update.effective_message     # Same as update.message
```

## Context Object Properties

### `context` (CallbackContext)
```python
context.bot                  # Bot instance for API calls
context.args                 # List of command arguments
context.user_data            # Persistent user data (dict)
context.chat_data            # Persistent chat data (dict)
context.bot_data             # Global bot data (dict)
```

## Message Methods

### Reply Methods
```python
# Basic text reply
update.message.reply_text("Hello!")

# Reply with markup
update.message.reply_text("Choose:", reply_markup=keyboard)

# Reply with HTML formatting
update.message.reply_html("<b>Bold</b> text")

# Reply with Markdown
update.message.reply_markdown("*Italic* text")
```

### Send Methods (via context.bot)
```python
# Send to specific chat
context.bot.send_message(chat_id=123, text="Hello")

# Send photo
context.bot.send_photo(chat_id=123, photo=open('image.jpg', 'rb'))

# Send document
context.bot.send_document(chat_id=123, document=open('file.pdf', 'rb'))
```

## Handler Types Quick Reference

### Command Handlers
```python
from telegram.ext import CommandHandler

# Basic command
dp.add_handler(CommandHandler("command", handler_function))

# Command with arguments
def echo(update, context):
    text = " ".join(context.args)
    update.message.reply_text(text)

dp.add_handler(CommandHandler("echo", echo))
```

### Message Handlers
```python
from telegram.ext import MessageHandler, Filters

# Text messages (non-commands)
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler))

# Photos
dp.add_handler(MessageHandler(Filters.photo, photo_handler))

# Documents
dp.add_handler(MessageHandler(Filters.document, document_handler))

# Audio
dp.add_handler(MessageHandler(Filters.audio, audio_handler))
```

### Callback Query Handlers
```python
from telegram.ext import CallbackQueryHandler

def button_click(update, context):
    query = update.callback_query
    query.answer()  # Acknowledge
    query.edit_message_text(f"You clicked: {query.data}")

dp.add_handler(CallbackQueryHandler(button_click))
```

## Inline Keyboards Quick Reference

### Basic Inline Keyboard
```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [
    [InlineKeyboardButton("Button 1", callback_data='1')],
    [InlineKeyboardButton("Button 2", callback_data='2')]
]
reply_markup = InlineKeyboardMarkup(keyboard)
update.message.reply_text('Choose:', reply_markup=reply_markup)
```

### URL Buttons
```python
keyboard = [[InlineKeyboardButton("Visit Site", url='https://example.com')]]
reply_markup = InlineKeyboardMarkup(keyboard)
```

## Regular Keyboards Quick Reference

### Custom Keyboard
```python
from telegram import KeyboardButton, ReplyKeyboardMarkup

keyboard = [
    [KeyboardButton("Option 1"), KeyboardButton("Option 2")],
    [KeyboardButton("Option 3")]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
update.message.reply_text('Choose:', reply_markup=reply_markup)
```

### Remove Keyboard
```python
from telegram import ReplyKeyboardRemove

update.message.reply_text('Keyboard removed', reply_markup=ReplyKeyboardRemove())
```

## Error Handling Quick Reference

### Basic Error Handler
```python
def error_handler(update, context):
    logger.warning(f'Update {update} caused error {context.error}')

dp.add_error_handler(error_handler)
```

### Try-Catch in Handlers
```python
def safe_handler(update, context):
    try:
        # Your handler logic
        update.message.reply_text("Success!")
    except Exception as e:
        update.message.reply_text("An error occurred")
        logger.error(f"Handler error: {e}")
```

## Environment Variables

### Required
```bash
BOT_TOKEN=your_telegram_bot_token
```

### Optional
```bash
WEBHOOK_URL=https://your-domain.com/webhook
USE_WEBHOOK=true
DEBUG=false
LOG_LEVEL=INFO
PORT=8443
```

## File Operations Quick Reference

### Download Files
```python
def handle_document(update, context):
    file = context.bot.get_file(update.message.document.file_id)
    file.download('downloaded_file.ext')
```

### Send Files
```python
# Send local file
context.bot.send_document(chat_id=update.effective_chat.id, 
                         document=open('file.pdf', 'rb'))

# Send file with custom filename
context.bot.send_document(chat_id=update.effective_chat.id,
                         document=open('file.pdf', 'rb'),
                         filename='custom_name.pdf')
```

## Logging Quick Setup

```python
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
```

## User Information Quick Access

### User Properties
```python
user = update.effective_user

user.id                      # Unique user ID
user.first_name             # User's first name
user.last_name              # User's last name (optional)
user.username               # Username (optional)
user.language_code          # User's language
user.is_bot                 # Boolean: is user a bot
```

### Chat Properties
```python
chat = update.effective_chat

chat.id                     # Unique chat ID
chat.type                   # 'private', 'group', 'supergroup', 'channel'
chat.title                  # Chat title (for groups)
chat.username               # Chat username (optional)
```

## Common Patterns

### Command with Arguments
```python
def command_with_args(update, context):
    if not context.args:
        update.message.reply_text("Usage: /command <arg1> <arg2>")
        return
    
    arg1, arg2 = context.args[0], context.args[1]
    update.message.reply_text(f"Args: {arg1}, {arg2}")
```

### User Data Storage
```python
def save_user_data(update, context):
    context.user_data['name'] = update.message.text
    update.message.reply_text("Name saved!")

def get_user_data(update, context):
    name = context.user_data.get('name', 'Unknown')
    update.message.reply_text(f"Your name: {name}")
```

### Admin-Only Commands
```python
ADMIN_IDS = [123456789, 987654321]

def admin_command(update, context):
    if update.effective_user.id not in ADMIN_IDS:
        update.message.reply_text("Not authorized")
        return
    
    update.message.reply_text("Admin command executed")
```

## Webhook vs Polling

### Polling (Current Implementation)
```python
updater.start_polling()
updater.idle()
```

### Webhook
```python
updater.start_webhook(
    listen="0.0.0.0",
    port=8443,
    url_path=token,
    webhook_url=f"https://yoursite.com/{token}"
)
updater.idle()
```

## Testing Quick Reference

### Mock Update Object
```python
from unittest.mock import Mock

update = Mock()
context = Mock()
update.message.reply_text = Mock()

# Test your handler
your_handler(update, context)

# Assert
update.message.reply_text.assert_called_with("Expected message")
```

This quick reference provides immediate access to the most commonly used APIs and patterns in the Telegram bot codebase.