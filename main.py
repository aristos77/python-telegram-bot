from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text("✅ Бот на Updater работает!")

def main():
    updater = Updater(token=os.environ.get("BOT_TOKEN"), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    import os
    main()
