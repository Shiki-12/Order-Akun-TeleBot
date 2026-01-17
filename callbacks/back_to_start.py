import db
import config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

PATTERN = "^back_to_start$"

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query 
    await query.answer()

    user = update.effective_user
    user_id = user.id
    username = f"@{user.username}" if user.username else "Tidak ada"
    
   
    total_stok = db.get_total_accounts_count()

    file_id = config.BANNER_FILE_ID 

    caption_text = (
        f"👋 <b>Halo {user.first_name}!</b>\n"
        f"Selamat Datang di <b>Premium Store</b>\n\n"
        f"🆔 <b>User Info:</b>\n"
        f"├ ID: <code>{user_id}</code>\n"
        f"├ Username: {username}\n"
        f"└ Transaksi: Rp 0\n\n"
        f"📊 <b>Bot Stats:</b>\n"
        f"├ Terjual: 0 pcs\n"
        f"├ Total Transaksi: Rp 0\n"
        f"└ Stok Ready: <code>{total_stok}</code> Akun\n\n"
        f"🚀 <b>Shortcuts:</b>\n"
        f"/accounts - Untuk melihat stok produk"
    )
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 List Produk", callback_data='list_produk')],
        [InlineKeyboardButton("❓ Cara Order", callback_data='how_to_order')]
    ])

    await query.edit_message_caption(
        caption=caption_text, 
        parse_mode='HTML', 
        reply_markup=reply_markup
    )