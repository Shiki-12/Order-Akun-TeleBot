import db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

PATTERN = "^back_to_start$"

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    total_stok = db.get_total_accounts_count()
    caption_start = (
        f"👋 <b>Halo {update.effective_user.first_name}!</b>\n"
        f"Selamat Datang Kembali di <b>Premium Store</b>\n\n"
        f"📊 <b>Bot Stats:</b>\n"
        f"└ Stok Ready: <code>{total_stok}</code> Akun\n\n"
        f"Silakan pilih menu di bawah ini:"
    )
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 List Produk", callback_data='list_produk')],
        [InlineKeyboardButton("❓ Cara Order", callback_data='how_to_order')]
    ])
    await query.edit_message_caption(caption=caption_start, parse_mode='HTML', reply_markup=reply_markup)
