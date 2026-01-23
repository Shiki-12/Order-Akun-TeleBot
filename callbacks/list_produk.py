import db
import config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

PATTERN = "^list_produk$"

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. Definisikan query
    query = update.callback_query
    
    # 2. AMAN: Hanya panggil answer() jika ini benar-benar callback/tombol
    if query:
        await query.answer()

    # 3. Ambil data kategori dari database
    categories = db.get_unique_categories()
    
    # 4. Siapkan logika tampilan (Teks & Keyboard)
    if not categories:
        text = "<b>❌ Maaf, saat ini belum ada produk yang tersedia.</b>"
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data='back_to_start')]])
    else:
        text = "<b>📦 DAFTAR KATEGORI PRODUK</b>\n"
        text += "<i>Silakan pilih kategori untuk melihat detail:</i>\n\n"
        
        keyboard = []
        for category, count in categories:
            text += f"▪️ <b>{category.upper()}</b> (Stok: <code>{count}</code>)\n"
            keyboard.append([InlineKeyboardButton(f"Beli {category.upper()}", callback_data=f"detail_{category}")])
        
        keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data='back_to_start')])
        reply_markup = InlineKeyboardMarkup(keyboard)

    # 5. LOGIKA PENGIRIMAN (Penentu Error Syntax tadi)
    if query:
        # Jika ditekan dari tombol inline (Edit pesan yang ada)
        await query.edit_message_caption(
            caption=text,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    else:
        # Jika dari teks/Reply Keyboard (Kirim pesan baru dengan foto)
        await update.message.reply_photo(
            photo=config.BANNER_FILE_ID,
            caption=text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )