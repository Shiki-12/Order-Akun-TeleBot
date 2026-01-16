from telegram import Update
from telegram.ext import ContextTypes
import db
from config import RESTOCK_ALLOWED

DESCRIPTION = "Add account: /restock <email> <user> <pass> [owner only]"

async def restock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in RESTOCK_ALLOWED:
        await update.message.reply_text("You don't have permission to use this command.")
        return

    if len(context.args) != 3:
        await update.message.reply_text(
            "<b>❌ Format Salah!</b>\n\n"
            "Gunakan format: <code>/restock [email] [kategori] [password]</code>\n"
            "Contoh: <code>/restock user@mail.com netflix pass123</code>",
            parse_mode='HTML' # Gunakan HTML agar konsisten
        )
        return
    
    email = context.args[0]
    username = context.args[1]
    password = context.args[2]

    try:
        db.add_account(email, username, password)
        await update.message.reply_text(f"Account saved for **{username}**!", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Database error: {e}")