from telegram import Update
from telegram.ext import ContextTypes
import db

DESCRIPTION = "List total stocked accounts"

def get_stock_message():
    rows = db.get_all_accounts()

    if not rows:
        return "No accounts found in database."

    # Group by username/category and count
    stock_counts = {}
    for email, user, pwd, cat in rows:
        key = (user, cat)
        stock_counts[key] = stock_counts.get(key, 0) + 1

    # Format the message
    message = "<b>📊 STOK SAAT INI:</b>\n\n"
    
    for i, ((username, category), count) in enumerate(stock_counts.items(), 1):
        cat_str = f" [<code>{category.upper()}</code>]" if category else ""
        message += f"{i}. <b>{username}</b>{cat_str} | Stok: <code>{count}</code>\n"

    message += f"\n<b>Total:</b> {len(rows)} account(s)"
    return message

async def accounts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = get_stock_message()
    await update.message.reply_text(message, parse_mode='HTML')