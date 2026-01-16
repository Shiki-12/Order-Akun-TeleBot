from telegram import Update
from telegram.ext import ContextTypes
import db

DESCRIPTION = "Add account: /restock <email> <user> <pass>"

async def restock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 3:
        await update.message.reply_text(
            "Error: You must provide exactly 3 items.\n"
            "Usage: `/restock <email> <username> <password>`",
            parse_mode='Markdown'
        )
        return

    email = context.args[0]
    username = context.args[1]
    password = context.args[2]

    try:
        db.add_account(email, username, password)
        await update.message.reply_text(f"Account saved for **{username}**!", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Database error: {e}")