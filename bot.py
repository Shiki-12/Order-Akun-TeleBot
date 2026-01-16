import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1. Load the variables from the .env file
load_dotenv()

# 2. Get the token securely
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Safety check: Ensure the token was loaded
if not TOKEN:
    raise ValueError("No TELEGRAM_TOKEN found in .env file")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Hello! I am a bot created with Python.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I can only say hello for now! Try typing /start")

if __name__ == '__main__':
    print("Bot is starting...")
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is polling...")
    app.run_polling()