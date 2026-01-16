from telegram import Update
from telegram.ext import ContextTypes
import db
import config

DESCRIPTION = "Start the bot and get welcome message"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    total_stok = db.get_total_accounts_count()
    nama_user = update.effective_user.first_name
    
  
    file_id = config.BANNER_FILE_ID

    caption_text = (
        f"👋 **Halo {nama_user}!**\n\n"
        f"Selamat datang di **Premium Store**.\n"
        f"Kami menyediakan berbagai akun premium dengan harga terjangkau.\n\n"
        f"📊 **Statistik Stok Saat Ini:**\n"
        f"• Total Akun Ready: `{total_stok}`\n\n"
        f"Gunakan /help untuk melihat cara order."
    )

    if file_id:
        await update.message.reply_photo(
            photo=file_id,
            caption=caption_text,
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(caption_text, parse_mode='Markdown')