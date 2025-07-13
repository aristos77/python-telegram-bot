import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from bs4 import BeautifulSoup
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Или вставь прямо строкой

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пришли ссылку на сайт, я создам таблицу с данными.")

# Обработка входящих ссылок
async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        titles = [tag.text.strip() for tag in soup.find_all("h1")]
        table = "\n".join(f"- {t}" for t in titles) or "Заголовков H1 не найдено."
        await update.message.reply_text(f"Вот что я нашел:\n{table}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

async def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
