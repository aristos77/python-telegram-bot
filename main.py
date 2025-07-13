import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Показать топ-10", callback_data="show_top")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "show_top":
        # Пример парсинга сайта
        url = "https://www.officialcharts.com/new-releases/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Заглушка — покажем фейковые треки
        tracks = [f"Artist {i} – Song {i}" for i in range(1, 11)]
        message = "\n".join([f"{i+1}. {track}" for i, track in enumerate(tracks)])
        await query.edit_message_text(f"🎵 Топ 10 синглов:\n{message}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
