from telegram import Update
from telegram.ext import ContextTypes
import db

DESCRIPTION = "List total stocked accounts"

async def accounts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = db.get_all_accounts()

    if not rows:
        await update.message.reply_text("No accounts found in database.")
        return

    # Group by username and count
    username_count = {}
    for email, user, pwd in rows:
        username_count[user] = username_count.get(user, 0) + 1

    # Format the message
    message = "**Current Stock:**\n\n"
    
    for i, (username, count) in enumerate(username_count.items(), 1):
        message += f"{i}. User: **{username}**\n"

    message += f"\n**Total:** {len(rows)} account(s)"
    await update.message.reply_text(message, parse_mode='Markdown')