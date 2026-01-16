import db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

PATTERN = "^detail_"

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category = query.data.split('_', 1)[1]
    price, desc = db.get_product_details(category)
    
    stok_count = 0
    all_categories = db.get_unique_categories()
    for cat, count in all_categories:
        if cat.lower() == category.lower():
            stok_count = count
            break

    text_detail = (
        f"<b>📦 DETAIL KATEGORI: {category.upper()}</b>\n\n"
        f"💰 <b>Harga:</b> Rp {price:,}\n"
        f"📊 <b>Stok Tersedia:</b> {stok_count} Akun\n"
        f"📝 <b>Deskripsi:</b>\n{desc}\n\n"
        f"<i>Apakah Anda ingin melanjutkan pembelian?</i>"
    )
    keyboard = [
        [InlineKeyboardButton(f"💳 Bayar Sekarang (Rp {price:,})", callback_data=f"buy_{category}")],
        [InlineKeyboardButton("⬅️ Kembali ke List", callback_data='list_produk')]
    ]
    await query.edit_message_caption(caption=text_detail, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
