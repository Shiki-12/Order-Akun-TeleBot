from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import db #
import config #

DESCRIPTION = "Start the bot and get welcome message"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = f"@{user.username}" if user.username else "Tidak ada"
    
    # Mengambil total stok dari database
    total_stok = db.get_total_accounts_count()
    file_id = config.BANNER_FILE_ID #

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

    # Struktur ReplyKeyboardMarkup
    keyboard = [
        [KeyboardButton("🏷️ Daftar Produk"), KeyboardButton("📦 Cek Stok")],
        [KeyboardButton("💰 Isi Saldo"), KeyboardButton("👤 Akun Saya")],
        [KeyboardButton("❓ Bantuan"), KeyboardButton("🎟️ Voucher")]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard, 
        resize_keyboard=True, 
        is_persistent=True 
    )

    # Struktur InlineKeyboardMarkup (Mirroring ReplyKeyboardMarkup)
    inline_keyboard = [
        [InlineKeyboardButton("🏷️ Daftar Produk", callback_data="list_produk"), InlineKeyboardButton("📦 Cek Stok", callback_data="check_stock")],
        [InlineKeyboardButton("💰 Isi Saldo", callback_data="add_balance"), InlineKeyboardButton("👤 Akun Saya", callback_data="my_account")],
        [InlineKeyboardButton("❓ Bantuan", callback_data="help"), InlineKeyboardButton("🎟️ Voucher", callback_data="voucher")]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)

    # Mengirim pesan dengan banner, caption, dan KEDUA keyboard (Reply & Inline)
    await update.message.reply_photo(
        photo=file_id,
        caption=caption_text,
        reply_markup=inline_markup, # Attach Inline Keyboard to the message
        parse_mode='HTML'
    )
    
    # Send a text message to ensure Reply Keyboard is visible/refreshed
    await update.message.reply_text(
        "Gunakan menu di bawah (Keyboard) atau tombol di atas (Inline).",
        reply_markup=reply_markup
    )