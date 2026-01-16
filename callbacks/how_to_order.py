from telegram import Update
from telegram.ext import ContextTypes

async def how_to_order_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_caption(
        caption="<b>Cara Order:</b>\n1. Klik List Produk\n2. Pilih Akun\n3. Bayar via QRIS\n4. Akun terkirim otomatis.",
        parse_mode='HTML'
    )
