import html # Tambahkan import ini
from telegram import Update
from telegram.ext import ContextTypes
from config import RESTOCK_ALLOWED

DESCRIPTION = "Get list of available commands"

def get_help_message(command_list, user_id):
    if not command_list:
        return "No commands found."

    # Gunakan tag <b> untuk HTML
    help_text = "<b>Available Commands:</b>\n\n"
    
    for cmd in command_list:
        if cmd.command == "restock" and user_id not in RESTOCK_ALLOWED:
            continue
        
        # Gunakan html.escape agar karakter < > tidak dianggap tag HTML
        safe_description = html.escape(cmd.description)
        help_text += f"/{cmd.command} - {safe_description}\n"
    
    return help_text

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    commands = context.bot_data.get("command_list", [])
    
    help_text = get_help_message(commands, user_id)

    await update.message.reply_text(help_text, parse_mode='HTML')