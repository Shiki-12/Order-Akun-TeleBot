from telegram import Update
from telegram.ext import ContextTypes
import db
from config import RESTOCK_ALLOWED # Mengambil daftar admin dari config

DESCRIPTION = "Atur harga produk: /setharga <nama> <harga> <deskripsi>"

async def setprice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Cek izin akses (hanya admin/owner)
    if user_id not in RESTOCK_ALLOWED:
        await update.message.reply_text("❌ Anda tidak memiliki izin untuk mengatur harga.")
        return

    # Validasi jumlah argumen
    if len(context.args) < 2:
        await update.message.reply_text(
            "<b>Format Salah!</b>\n"
            "Gunakan: <code>/setharga [nama_produk] [harga] [deskripsi...]</code>\n\n"
            "Contoh: <code>/setharga netflix 50000 Akun Premium 1 Bulan</code>",
            parse_mode='HTML'
        )
        return

    product_name = context.args[0].lower()
    
    # Validasi harga harus angka
    try:
        price = int(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Harga harus berupa angka tanpa titik/koma (Contoh: 50000).")
        return

    # Mengambil sisa argumen sebagai deskripsi
    description = " ".join(context.args[2:]) if len(context.args) > 2 else "Tidak ada deskripsi."

    try:
        db.set_product_price(product_name, price, description)
        await update.message.reply_text(
            f"✅ <b>Berhasil Diperbarui!</b>\n\n"
            f"📦 Produk: <code>{product_name.upper()}</code>\n"
            f"💰 Harga: Rp {price:,}\n"
            f"📝 Deskripsi: {description}",
            parse_mode='HTML'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Terjadi kesalahan database: {e}")