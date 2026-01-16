import db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

PATTERN = "^list_produk$"

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    products = db.get_unique_products()
    
    if not products:
        await query.edit_message_caption(
            caption="<b>❌ Maaf, saat ini belum ada produk yang tersedia.</b>",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data='back_to_start')]])
        )
        return

    text = "<b>📦 DAFTAR PRODUK READY</b>\n"
    text += "<i>Silakan pilih produk untuk melihat detail:</i>\n\n"
    
    keyboard = []
    for name, count in products:
        text += f"▪️ <b>{name.upper()}</b> (Stok: <code>{count}</code>)\n"
        keyboard.append([InlineKeyboardButton(f"Beli {name.upper()}", callback_data=f"detail_{name}")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data='back_to_start')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_caption(
        caption=text,
        parse_mode='HTML',
        reply_markup=reply_markup
    )
