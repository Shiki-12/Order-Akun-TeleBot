from telegram import Update
from telegram.ext import ContextTypes
from config import RESTOCK_ALLOWED

DESCRIPTION = "Get list of available commands"

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    commands = context.bot_data.get("command_list", [])
    
    if not commands:
        await update.message.reply_text("No commands found.")
        return

    help_text = "**Available Commands:**\n\n"
    
    for cmd in commands:
        if cmd.command == "restock" and user_id not in RESTOCK_ALLOWED:
            continue
        help_text += f"/{cmd.command} - {cmd.description}\n"

    await update.message.reply_text(help_text, parse_mode='Markdown')