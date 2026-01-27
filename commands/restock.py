import csv
from io import StringIO
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
import db
from config import RESTOCK_ALLOWED

# Deskripsi perintah diperbarui agar mencakup harga dan deskripsi
DESCRIPTION = "Restock: /restock <email> <user> <pass> <cat> [harga] [deskripsi]"

async def restock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Validasi izin akses admin
    if user_id not in RESTOCK_ALLOWED:
        await update.message.reply_text("❌ Anda tidak memiliki izin untuk menggunakan perintah ini.")
        return

    # LOGIKA 1: PENANGANAN FILE CSV (BULK RESTOCK)
    if update.message.document:
        document = update.message.document
        file_name = document.file_name
        
        if not file_name.lower().endswith('.csv'):
             await update.message.reply_text("❌ Mohon upload file dalam format .CSV")
             return

        try:
            new_file = await context.bot.get_file(document.file_id)
            file_content = await new_file.download_as_bytearray()
            decoded_content = file_content.decode('utf-8')
            
            csv_file = StringIO(decoded_content)
            reader = csv.DictReader(csv_file)
            
            # Validasi header minimal
            required_headers = {'email', 'username', 'password', 'category'}
            if not reader.fieldnames or not required_headers.issubset(set(reader.fieldnames)):
                 await update.message.reply_text(f"❌ Format CSV Salah. Header wajib: {', '.join(required_headers)}")
                 return

            success_count = 0
            error_count = 0
            errors = []
            
            for row in reader:
                try:
                    # Ambil harga dan deskripsi jika tersedia di kolom CSV (opsional)
                    price = int(row['price']) if 'price' in row and row['price'] else None
                    description = row.get('description', None)
                    
                    # Panggil fungsi db yang sudah diperbarui
                    db.add_account(
                        row['email'], 
                        row['username'], 
                        row['password'], 
                        row['category'],
                        price,
                        description
                    )
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    errors.append(f"{row.get('username', 'Unknown')}: {str(e)}")
            
            msg = f"<b>✅ Restock CSV Selesai</b>\n\nBerhasil: {success_count}\nGagal: {error_count}"
            if errors:
                msg += "\n\nTerjadi Error:\n" + "\n".join(errors[:5])
                
            await update.message.reply_text(msg, parse_mode='HTML')
            return
        except Exception as e:
            await update.message.reply_text(f"❌ Gagal memproses file: {e}")
            return

    # LOGIKA 2: PENANGANAN TEKS MANUAL
    args = context.args if context.args is not None else []

    # Validasi jumlah argumen minimal (4)
    if len(args) < 4:
        await update.message.reply_text(
            "<b>❌ Format Salah!</b>\n\n"
            "Cara 1: Upload CSV (email,username,password,category,[price],[description])\n"
            "Cara 2: <code>/restock [email] [user] [pass] [cat] [harga] [deskripsi...]</code>\n\n"
            "<i>Contoh: /restock user@mail.com shiki 123 Netflix 50000 Premium 1 Bulan</i>",
            parse_mode='HTML'
        )
        return
    
    email = args[0]
    username = args[1]
    password = args[2]
    category = args[3]
    
    # Ambil harga dan deskripsi jika ada (argumen ke-5 dan seterusnya)
    price = None
    description = None
    
    if len(args) >= 5:
        try:
            price = int(args[4])
        except ValueError:
            await update.message.reply_text("❌ Harga harus berupa angka tanpa titik/koma.")
            return

    if len(args) >= 6:
        description = " ".join(args[5:])

    try:
        # Integrasi harga ke database saat restock
        db.add_account(email, username, password, category, price, description)
        
        info_msg = f"✅ Akun <b>{username}</b> berhasil disimpan ke kategori <b>{category.upper()}</b>!"
        if price is not None:
            info_msg += f"\n💰 Harga kategori diperbarui: Rp {price:,}"
            
        await update.message.reply_text(info_msg, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"❌ Database error: {e}")

# Definisi Handlers
HANDLERS = [
    CommandHandler("restock", restock_command),
    MessageHandler(filters.Document.ALL & filters.CaptionRegex(r"^/restock"), restock_command)
]