from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

PATTERN = "^how_to_order$"

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text_order = (
        "<b>❓ CARA ORDER:</b>\n\n"
        "1. Pilih produk di <b>List Produk</b>\n"
        "2. Klik <b>Bayar Sekarang</b>\n"
        "3. Selesaikan pembayaran\n"
        "4. Akun dikirim otomatis oleh Bot."
    )
    await query.edit_message_caption(
        caption=text_order, 
        parse_mode='HTML', 
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data='back_to_start')]])
    )
