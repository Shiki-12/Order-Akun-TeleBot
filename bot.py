import os
import importlib
from dotenv import load_dotenv
from telegram import BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, Application

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

async def post_init(application: Application):
    commands = load_handlers(application)
    
    application.bot_data["command_list"] = commands
    
    await application.bot.set_my_commands(commands)

if __name__ == '__main__':
    print("Bot is starting...")
    
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    print("Bot is polling...")
    app.run_polling()