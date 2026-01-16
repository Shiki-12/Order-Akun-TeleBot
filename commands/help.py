from telegram import Update
from telegram.ext import ContextTypes

DESCRIPTION = "Get list of available commands"

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is the help message from help.py")