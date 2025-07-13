import logging
import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь /top, чтобы получить топ синглов.")

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://www.billboard.com/charts/hot-100/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    results = soup.select("li.o-chart-results-list__item h3")
    top_10 = [r.get_text(strip=True) for r in results[:10]]

    message = "🎵 Топ 10 синглов:\n\n" + "\n".join(f"{i+1}. {title}" for i, title in enumerate(top_10))
    await update.message.reply_text(message)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("top", top))
    app.run_polling()

if __name__ == "__main__":
    main()
