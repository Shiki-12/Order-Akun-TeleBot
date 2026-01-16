from telegram import Update
from telegram.ext import ContextTypes
import db

DESCRIPTION = "List all saved accounts"

async def accounts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = db.get_all_accounts()

    if not rows:
        await update.message.reply_text("No accounts found in database.")
        return

    # Format the message
    message = "**Current Stock:**\n\n"
    
    for i, row in enumerate(rows, 1):
        # row is a tuple: (email, username, password)
        email, user, pwd = row
        message += f"{i}. **User:** `{user}` | **Email:** `{email}` | **Pass:** `{pwd}`\n"

    await update.message.reply_text(message, parse_mode='Markdown')