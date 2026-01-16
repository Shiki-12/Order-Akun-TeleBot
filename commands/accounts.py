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
    # Group by username/category and count
    stock_counts = {}
    for email, user, pwd, cat in rows:
        key = (user, cat)
        stock_counts[key] = stock_counts.get(key, 0) + 1

    # Format the message
    message = "<b>Current Stock:</b>\n\n"
    
    for i, ((username, category), count) in enumerate(stock_counts.items(), 1):
        cat_str = f" ({category})" if category else ""
        message += f"{i}. User: <b>{username}</b>{cat_str} | Stok: {count}\n"

    message += f"\n<b>Total:</b> {len(rows)} account(s)"
    await update.message.reply_text(message, parse_mode='HTML')