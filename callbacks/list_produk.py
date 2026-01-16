from telegram import Update
from telegram.ext import ContextTypes

async def list_produk_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_caption(
        caption="<b>Daftar Produk:</b>\n1. Netflix\n2. Spotify\n\nSilakan pilih nomor...",
        parse_mode='HTML'
    )
