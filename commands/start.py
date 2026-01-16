from telegram import Update
from telegram.ext import ContextTypes

DESCRIPTION = "Start the bot and get welcome message"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello World!")