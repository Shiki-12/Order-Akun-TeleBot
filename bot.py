import os
import importlib
import random
import string
from dotenv import load_dotenv

# Telegram Imports
from telegram import BotCommand, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    Application, 
    CallbackQueryHandler, 
    ContextTypes
)

# Local Imports
import db

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("No TELEGRAM_TOKEN found in .env file")

def load_handlers(application: Application):
    """
    Scans /commands, loads handlers, and reads the DESCRIPTION variable.
    """
    command_dir = "commands"
    loaded_commands = []

    if not os.path.exists(command_dir):
        os.makedirs(command_dir)

    command_files = [f for f in os.listdir(command_dir) if f.endswith('.py') and not f.startswith('__')]

    for filename in command_files:
        module_name = f"{command_dir}.{filename[:-3]}"
        command_name = filename[:-3]

        try:
            module = importlib.import_module(module_name)
            func_name = f"{command_name}_command"
            
            if hasattr(module, func_name):
                handler_func = getattr(module, func_name)
                application.add_handler(CommandHandler(command_name, handler_func))
                description = getattr(module, "DESCRIPTION", "No description provided")
                loaded_commands.append(BotCommand(command_name, description))
                print(f"Loaded: /{command_name} - {description}")
            else:
                print(f"Skipped {filename}: Missing function '{func_name}'")

        except Exception as e:
            print(f"Failed to load {filename}: {e}")


    return loaded_commands

def load_callback_handlers(application: Application):
    """
    Scans /callbacks, loads handlers for CallbackQueryHandler.
    Matches filename to callback_data.
    """
    callback_dir = "callbacks"
    
    if not os.path.exists(callback_dir):
        print(f"Directory '{callback_dir}' not found. Skipping callback loading.")
        return

    callback_files = [f for f in os.listdir(callback_dir) if f.endswith('.py') and not f.startswith('__')]

    for filename in callback_files:
        module_name = f"{callback_dir}.{filename[:-3]}"
        callback_data = filename[:-3]

        try:
            module = importlib.import_module(module_name)
            func_name = f"{callback_data}_callback"
            
            if hasattr(module, func_name):
                handler_func = getattr(module, func_name)
                # Using regex pattern to match exact callback data
                pattern = f"^{callback_data}$"
                application.add_handler(CallbackQueryHandler(handler_func, pattern=pattern))
                print(f"Loaded callback: {callback_data}")
            else:
                print(f"Skipped {filename}: Missing function '{func_name}'")

        except Exception as e:
            print(f"Failed to load callback {filename}: {e}")

async def post_init(application: Application):
    commands = load_handlers(application)
    application.bot_data["command_list"] = commands
    await application.bot.set_my_commands(commands)
    
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    await query.answer()
    
    # Bungkus seluruh logika dalam try-except untuk menangani error Telegram
    try:
        # MENU: LIST PRODUK
        if query.data == 'list_produk':
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

        # MENU: KEMBALI KE START
        elif query.data == 'back_to_start':
            total_stok = db.get_total_accounts_count()
            caption_start = (
                f"👋 <b>Halo {update.effective_user.first_name}!</b>\n"
                f"Selamat Datang Kembali di <b>Premium Store</b>\n\n"
                f"📊 <b>Bot Stats:</b>\n"
                f"└ Stok Ready: <code>{total_stok}</code> Akun\n\n"
                f"Silakan pilih menu di bawah ini:"
            )
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 List Produk", callback_data='list_produk')],
                [InlineKeyboardButton("❓ Cara Order", callback_data='how_to_order')]
            ])
            await query.edit_message_caption(caption=caption_start, parse_mode='HTML', reply_markup=reply_markup)

        # MENU: CARA ORDER
        elif query.data == 'how_to_order':
            text_order = (
                "<b>❓ CARA ORDER:</b>\n\n"
                "1. Pilih produk di <b>List Produk</b>\n"
                "2. Klik <b>Bayar Sekarang</b>\n"
                "3. Selesaikan pembayaran\n"
                "4. Akun dikirim otomatis oleh Bot."
            )
            await query.edit_message_caption(
                caption=text_order, 
                parse_mode='HTML', 
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data='back_to_start')]])
            )

        # MENU: DETAIL PRODUK
        elif query.data.startswith('detail_'):
            product_name = query.data.split('_')[1]
            price, desc = db.get_product_details(product_name)
            
            stok_count = 0
            all_stok = db.get_unique_products()
            for name, count in all_stok:
                if name.lower() == product_name.lower():
                    stok_count = count
                    break

            text_detail = (
                f"<b>📦 DETAIL PRODUK: {product_name.upper()}</b>\n\n"
                f"💰 <b>Harga:</b> Rp {price:,}\n"
                f"📊 <b>Stok Tersedia:</b> {stok_count} Akun\n"
                f"📝 <b>Deskripsi:</b>\n{desc}\n\n"
                f"<i>Apakah Anda ingin melanjutkan pembelian?</i>"
            )
            keyboard = [
                [InlineKeyboardButton(f"💳 Bayar Sekarang (Rp {price:,})", callback_data=f"buy_{product_name}")],
                [InlineKeyboardButton("⬅️ Kembali ke List", callback_data='list_produk')]
            ]
            await query.edit_message_caption(caption=text_detail, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

        # MENU: PROSES BELI (INVOICE)
        elif query.data.startswith('buy_'):
            product_name = query.data.split('_')[1]
            price, desc = db.get_product_details(product_name)
            
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            order_id = f"INV-{random_str}"
            
            db.create_order(order_id, user_id, product_name, price)
            
            text_invoice = (
                f"<b>📝 PESANAN DIBUAT!</b>\n\n"
                f"📌 <b>Order ID:</b> <code>{order_id}</code>\n"
                f"📦 <b>Produk:</b> {product_name.upper()}\n"
                f"💰 <b>Total Bayar:</b> Rp {price:,}\n\n"
                f"⚠️ <i>Langkah selanjutnya adalah generate QRIS.\n"
                f"Mohon tunggu integrasi Payment Gateway.</i>"
            )
            keyboard = [[InlineKeyboardButton("✅ Konfirmasi (Demo)", callback_data=f"confirm_{order_id}")]]
            await query.edit_message_caption(caption=text_invoice, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

    except BadRequest as e:
        if "Message is not modified" in str(e):
            pass
        else:
            print(f"Error Telegram: {e}")

if __name__ == '__main__':
    print("Bot is starting...")
    db.setup_db()
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    print("Bot is polling...")
    app.run_polling()