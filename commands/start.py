from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
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

    # Struktur ReplyKeyboardMarkup sesuai referensi gambar yang Anda inginkan
    # Pastikan menggunakan KeyboardButton, bukan InlineKeyboardButton
    keyboard = [
        [KeyboardButton("🏷️ Daftar Produk"), KeyboardButton("💰 Sisa Saldo: Rp 0")],
        [KeyboardButton("📦 Cek Stok")],
        [KeyboardButton("1"), KeyboardButton("2"), KeyboardButton("3"), KeyboardButton("4"), KeyboardButton("5")],
        [KeyboardButton("6")],
        [KeyboardButton("💰 Isi Saldo"), KeyboardButton("👤 Akun Saya")],
        [KeyboardButton("❓ Bantuan"), KeyboardButton("🎟️ Voucher")]
    ]

    # PERBAIKAN: Ganti 'persistent' menjadi 'is_persistent'
    reply_markup = ReplyKeyboardMarkup(
        keyboard, 
        resize_keyboard=True, 
        is_persistent=True 
    )

    # Mengirim pesan dengan banner dan keyboard baru
    await update.message.reply_photo(
        photo=file_id,
        caption=caption_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )