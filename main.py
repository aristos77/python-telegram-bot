from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

def fetch_tracks():
    url = "https://www.officialcharts.com/new-releases/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tracks = [el.get_text(strip=True) for el in soup.select("h3")]
    return tracks

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔍 Показать 10 треков", callback_data="show")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать! Нажмите кнопку ниже для получения новых синглов:", reply_markup=reply_markup)

async def show_tracks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tracks = fetch_tracks()
    top_10 = "\n".join(tracks[:10]) or "Не найдено"
    await query.edit_message_text(text=f"🎵 Топ 10 синглов:

{top_10}")

async def parse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tracks = fetch_tracks()
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Укажи исполнителя: /parse Eminem")
        return
    filtered = [t for t in tracks if text.lower() in t.lower()]
    if filtered:
        await update.message.reply_text("\n".join(filtered[:10]))
    else:
        await update.message.reply_text("По запросу ничего не найдено.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("parse", parse))
    app.add_handler(CallbackQueryHandler(show_tracks, pattern="^show$"))
    app.run_polling()

if __name__ == "__main__":
    main()
