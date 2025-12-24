import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, DATA_FILE
from parser import update_schedule

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для уведомлений о отключениях ⚡")

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Покажем первые строки для примера
        text = "\n".join(data[:20])
    except Exception as e:
        text = "Расписание ещё не загружено."
    await update.message.reply_text(text)

async def refresh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Обновляю расписание…")
    data = update_schedule()
    await update.message.reply_text(f"График обновлён, строк: {len(data)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("schedule", schedule))
    app.add_handler(CommandHandler("refresh", refresh))
    app.run_polling()

if __name__ == "__main__":
    main()