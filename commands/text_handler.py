from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
# Impor fungsi dari file lain agar tidak menulis ulang logika
from commands.accounts import accounts_command
from callbacks.list_produk import callback_handler as list_produk_logic

DESCRIPTION = "Menangani input teks dari Reply Keyboard"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🏷️ Daftar Produk":
        from callbacks.list_produk import callback_handler
        import callbacks.list_produk as lp
        await lp.callback_handler(update, context) 

    elif text == "📦 Cek Stok":
        await accounts_command(update, context)

    elif text in ["1", "2", "3", "4", "5", "6"]:
        await update.message.reply_text(f"Anda memilih menu nomor {text}. Fitur ini sedang dikembangkan.")

    elif text == "❓ Bantuan":
        from commands.help import help_command
        await help_command(update, context)

    else:
        # Opsional: Beri tahu jika perintah tidak dikenal
        # await update.message.reply_text("Gunakan menu yang tersedia di bawah.")
        pass

# Eksport HANDLERS agar dibaca oleh bot.py
HANDLERS = [
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
]