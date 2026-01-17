from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import db
import config

DESCRIPTION = "Start the bot and get welcome message"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    # HANYA dua tombol ini yang tersisa
    keyboard = [
        [InlineKeyboardButton("🛒 List Produk", callback_data='list_produk')],
        [InlineKeyboardButton("❓ Cara Order", callback_data='how_to_order')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=file_id,
        caption=caption_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )