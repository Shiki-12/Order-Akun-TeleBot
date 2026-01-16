import os
from dotenv import load_dotenv
from telegram import BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, Application

from commands.start import start_command
from commands.help import help_command

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("Token Not Found, please create .env file or copy .env.example to .env and insert your own token")

# 1. Define the setup function
async def post_init(application: Application):
    """
    This function runs once when the bot starts.
    It tells Telegram to show these commands in the Menu button.
    """
    print("Setting up the Menu button...")
    
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Get help and instructions"),
    ]
    
    await application.bot.set_my_commands(commands)

if __name__ == '__main__':
    print("Bot is starting...")
    
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is polling...")
    app.run_polling()