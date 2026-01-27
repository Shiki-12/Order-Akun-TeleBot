from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters
import db
import config
from commands.accounts import accounts_command
from commands.help import help_command
from duitku_api import DuitkuAPI
import random
import string

DESCRIPTION = "Menangani input teks dari Reply Keyboard"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    
    # 1. NAVIGATION & START MENU
    if text == "⬅️ Kembali" or text == "🏠 Menu Utama":
        keyboard = [
            [KeyboardButton("🏷️ Daftar Produk"), KeyboardButton("📦 Cek Stok")],
            [KeyboardButton("💰 Isi Saldo"), KeyboardButton("👤 Akun Saya")],
            [KeyboardButton("❓ Bantuan"), KeyboardButton("🎟️ Voucher")]
        ]
        await update.message.reply_text(
            "🏠 <b>Menu Utama</b>",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True),
            parse_mode='HTML'
        )
        return

    # 2. LIST PRODUCT
    if text == "🏷️ Daftar Produk":
        categories = db.get_unique_categories()
        if not categories:
            await update.message.reply_text("❌ Belum ada produk yang tersedia.")
            return
        
        keyboard = []
        # Arrange in 2 columns
        row = []
        for category, count in categories:
            row.append(KeyboardButton(category.upper()))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
            
        keyboard.append([KeyboardButton("⬅️ Kembali")])
        
        await update.message.reply_text(
            "📂 <b>Pilih Kategori Produk:</b>",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
            parse_mode='HTML'
        )
        return

    # 3. STOCK CHECK
    elif text == "📦 Cek Stok":
        await accounts_command(update, context)
        return

    elif text == "❓ Bantuan":
        await help_command(update, context)
        return
        
    elif text == "💰 Isi Saldo":
        await update.message.reply_text("💰 Fitur isi saldo sedang dikembangkan. Hubungi admin.")
        return

    elif text == "👤 Akun Saya":
        user = update.effective_user
        msg = f"👤 <b>Info Akun</b>\nName: {user.first_name}\nID: <code>{user.id}</code>"
        await update.message.reply_text(msg, parse_mode='HTML')
        return

    # 4. PURCHASE FLOW: BUY BUTTON CLICKED
    if text.startswith("🛒 Beli "):
        category_raw = text.replace("🛒 Beli ", "").strip()
        # Find the actual casing in DB (e.g. Input: TIDAL -> DB: Tidal)
        category = db.get_actual_category_case(category_raw)
        
        price, _ = db.get_product_details(category)
        
        if price <= 0:
            await update.message.reply_text("⚠️ Produk tidak valid atau harga belum diset.")
            return

        # Generate Invoice
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        order_id = f"INV-{random_str}"
        
        dui = DuitkuAPI()
        # Use placeholder email or fetch from user_data if we had it
        email = "customer@example.com"
        
        resp = dui.create_invoice(order_id, price, category, email)
        
        if resp and 'paymentUrl' in resp:
            payment_url = resp['paymentUrl']
            ref_id = resp.get('reference', '')
            
            db.create_order(order_id, user_id, category, price, payment_url, ref_id)
            
            # Save order_id to session
            context.user_data['active_order_id'] = order_id
            
            msg = (
                f"📝 <b>TAGIHAN DIBUAT!</b>\n"
                f"Produk: <b>{category_raw}</b>\n"
                f"Total: <b>Rp {price:,}</b>\n\n"
                f"🔗 <a href='{payment_url}'>KLIK DISINI UNTUK BAYAR</a>\n\n"
                f"<i>Setelah bayar, tekan tombol Cek Status di bawah.</i>"
            )
            
            keyboard = [
                [KeyboardButton("🔄 Cek Status Pembayaran")],
                [KeyboardButton("❌ Batalkan / Kembali")]
            ]
            
            await update.message.reply_text(
                msg,
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text("⚠️ Gagal membuat tagihan. Coba lagi nanti.")
        return

    # 5. CHECK STATUS FLOW
    if text == "🔄 Cek Status Pembayaran":
        order_id = context.user_data.get('active_order_id')
        if not order_id:
            await update.message.reply_text("⚠️ Tidak ada transaksi aktif yang ditemukan.")
            return
            
        # Check Logic (Borrowed/Adapted from check_payment.py)
        dui = DuitkuAPI()
        
        # Check DB first (in case changed separately)
        order = db.get_order(order_id)
        if not order:
            await update.message.reply_text("⚠️ Data order tidak ditemukan.")
            return
            
        status = order[4] # status index
        product_name = order[2].lower() # Force lower to ensure matching with accounts table
        
        is_paid = False
        if status == 'SUCCESS':
            is_paid = True
        else:
            # Check API
            result = dui.check_transaction_status(order_id)
            if result and result.get("statusCode") == "00":
                db.update_order_status(order_id, 'SUCCESS')
                is_paid = True
        
        if is_paid:
            # Delivery Logic
            account = db.get_random_account(product_name)
            if account:
                acc_id, email, username, password = account
                
                # Match check_payment.py format
                msg_acc = (
                    f"✅ <b>PAYMENT RECEIVED!</b>\n"
                    f"Here is your account:\n\n"
                    f"📧 Email: <code>{email}</code>\n"
                    f"👤 User: <code>{username}</code>\n"
                    f"🔑 Pass: <code>{password}</code>\n\n"
                    f"<i>Thank you for purchasing!</i>"
                )
                db.delete_account(acc_id)
                
                # Clear active order
                if 'active_order_id' in context.user_data:
                    del context.user_data['active_order_id']
                
                # Back to Main Menu
                keyboard = [
                    [KeyboardButton("🏷️ Daftar Produk"), KeyboardButton("📦 Cek Stok")],
                    [KeyboardButton("💰 Isi Saldo"), KeyboardButton("👤 Akun Saya")],
                    [KeyboardButton("❓ Bantuan"), KeyboardButton("🎟️ Voucher")]
                ]
                await update.message.reply_text(
                    msg_acc,
                    reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
                    parse_mode='HTML'
                )
            else:
                 await update.message.reply_text(
                    f"✅ Payment Successful, but Stock Empty for '{product_name}'. Contact Admin.",
                    parse_mode='HTML'
                 )
        else:
            await update.message.reply_text("⏳ <b>Status: Belum Terbayar</b>\nSilakan lakukan pembayaran lalu cek lagi.", parse_mode='HTML')
            
        return

    if text == "❌ Batalkan / Kembali":
        if 'active_order_id' in context.user_data:
            del context.user_data['active_order_id']
        # Go back to main
        # Pass through to generic handler flow or recursion?
        # Just call the 'Kembali' handler logic manually
        # Repetitive code, but safe.
        keyboard = [
            [KeyboardButton("🏷️ Daftar Produk"), KeyboardButton("📦 Cek Stok")],
            [KeyboardButton("💰 Isi Saldo"), KeyboardButton("👤 Akun Saya")],
            [KeyboardButton("❓ Bantuan"), KeyboardButton("🎟️ Voucher")]
        ]
        await update.message.reply_text(
            "🏠 <b>Menu Utama</b> (Transaksi Dibatalkan)",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
            parse_mode='HTML'
        )
        return

    # 6. DYNAMIC CATEGORY DETECTION (If user clicks a Category Button)
    # Check if text matches a known category
    categories_raw = db.get_unique_categories()
    for cat, count in categories_raw:
        if text.upper() == cat.upper():
            # Show Product Detail
            price, desc = db.get_product_details(cat)
            msg = (
                f"📦 <b>{cat.upper()}</b>\n"
                f"💰 Harga: Rp {price:,}\n"
                f"📝 {desc}\n\n"
                f"Stok Tersedia: {count} pcs"
            )
            
            keyboard = [
                [KeyboardButton(f"🛒 Beli {cat.upper()}")],
                [KeyboardButton("⬅️ Kembali")]
            ]
            await update.message.reply_text(
                msg,
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
                parse_mode='HTML'
            )
            return

    # Fallback
    await update.message.reply_text("Maaf, perintah tidak dikenali atau sesi kadaluarsa.")

HANDLERS = [
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
]