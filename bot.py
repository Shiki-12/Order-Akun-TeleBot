import os
import importlib
from dotenv import load_dotenv

# Telegram Imports
from telegram import BotCommand, Update
from telegram.error import BadRequest
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    Application, 
    CallbackQueryHandler, 
    ContextTypes
)

# Local Imports
import db

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("No TELEGRAM_TOKEN found in .env file")

def load_handlers(application: Application):
    """
    Scans /commands, loads handlers, and reads the DESCRIPTION variable.
    """
    command_dir = "commands"
    loaded_commands = []

    command_files = [f for f in os.listdir(command_dir) if f.endswith('.py') and not f.startswith('__')]

    for filename in command_files:
        module_name = f"{command_dir}.{filename[:-3]}"
        command_name = filename[:-3]

        try:
            module = importlib.import_module(module_name)
            func_name = f"{command_name}_command"
            
            if hasattr(module, func_name):
                handler_func = getattr(module, func_name)
                application.add_handler(CommandHandler(command_name, handler_func))
                description = getattr(module, "DESCRIPTION", "No description provided")
                loaded_commands.append(BotCommand(command_name, description))
                print(f"Loaded: /{command_name} - {description}")
            else:
                print(f"Skipped {filename}: Missing function '{func_name}'")

        except Exception as e:
            print(f"Failed to load {filename}: {e}")


    return loaded_commands

def load_callback_handlers(application: Application):
    """
    Scans /callbacks, loads handlers dynamically based on PATTERN.
    """
    callback_dir = "callbacks"
    
    callback_files = [f for f in os.listdir(callback_dir) if f.endswith('.py') and not f.startswith('__')]

    for filename in callback_files:
        module_name = f"{callback_dir}.{filename[:-3]}"
        
        try:
            module = importlib.import_module(module_name)
            
            if hasattr(module, "callback_handler") and hasattr(module, "PATTERN"):
                original_handler = getattr(module, "callback_handler")
                pattern = getattr(module, "PATTERN")
                
                # Wrapper to handle "Message is not modified" error
                async def wrapped_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, handler=original_handler):
                    try:
                        await handler(update, context)
                    except BadRequest as e:
                        if "Message is not modified" in str(e):
                            pass
                        else:
                            print(f"Error Telegram: {e}")

                application.add_handler(CallbackQueryHandler(wrapped_handler, pattern=pattern))
                print(f"Loaded Callback: {filename} (Pattern: {pattern})")
            else:
                print(f"Skipped {filename}: Missing 'callback_handler' or 'PATTERN'")

        except Exception as e:
            print(f"Failed to load callback {filename}: {e}")

async def post_init(application: Application):
    commands = load_handlers(application)
    load_callback_handlers(application)
    application.bot_data["command_list"] = commands
    await application.bot.set_my_commands(commands)

if __name__ == '__main__':
    print("Bot is starting...")
    db.setup_db()
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    print("Bot is polling...")
    app.run_polling()