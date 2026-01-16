import db
import random
import string
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

PATTERN = "^buy_"

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_user.id
    await query.answer()

    product_name = query.data.split('_', 1)[1]
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
