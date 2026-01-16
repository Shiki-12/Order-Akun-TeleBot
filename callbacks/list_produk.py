import db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

PATTERN = "^list_produk$"

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    
    categories = db.get_unique_categories()
    
    if not categories:
        await query.edit_message_caption(
            caption="<b>❌ Maaf, saat ini belum ada produk yang tersedia.</b>",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data='back_to_start')]])
        )
        return

    text = "<b>📦 DAFTAR KATEGORI PRODUK</b>\n"
    text += "<i>Silakan pilih kategori untuk melihat detail:</i>\n\n"
    
    keyboard = []
    for category, count in categories:
        text += f"▪️ <b>{category.upper()}</b> (Stok: <code>{count}</code>)\n"
        keyboard.append([InlineKeyboardButton(f"Beli {category.upper()}", callback_data=f"detail_{category}")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data='back_to_start')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_caption(
        caption=text,
        parse_mode='HTML',
        reply_markup=reply_markup
    )
