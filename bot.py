import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

# Import functions from the commands folder
from commands.start import start_command
from commands.help import help_command

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("Token Not Found, please create .env file or copy .env.example to .env and insert your own token")

if __name__ == '__main__':
    print("Bot is starting...")
    
    app = ApplicationBuilder().token(TOKEN).build()

    # Link the imported functions to the commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is polling...")
    app.run_polling()