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

    category = query.data.split('_', 1)[1]
    price, desc = db.get_product_details(category)
    
    if price <= 0:
        await query.edit_message_caption(caption="⚠️ Product price is invalid (0). Please contact admin to set price.")
        return
    
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    order_id = f"INV-{random_str}"
    
    # Create Duitku Invoice
    from duitku_api import DuitkuAPI
    dui = DuitkuAPI()
    
    # User email (optional, use placeholder or ask user. For now using placeholder)
    email = "customer@example.com" 
    
    resp = dui.create_invoice(order_id, price, category, email)
    
    payment_url = "https://duitku.com" # Fallback
    if resp and 'paymentUrl' in resp:
        payment_url = resp['paymentUrl']
        ref_id = resp.get('reference', '') # Duitku Reference
        
        # Save to DB
        db.create_order(order_id, user_id, category, price, payment_url, ref_id)
        
        text_invoice = (
            f"<b>📝 INVOICE CREATED!</b>\n\n"
            f"📌 <b>Order ID:</b> <code>{order_id}</code>\n"
            f"📦 <b>Kategori:</b> {category.upper()}\n"
            f"💰 <b>Total Bayar:</b> Rp {price:,}\n\n"
            f"⚠️ <i>Please click the button below to pay.</i>"
        )
        keyboard = [
            [InlineKeyboardButton("🔗 Pay Now", url=payment_url)],
            [InlineKeyboardButton("🔄 Check Status", callback_data=f"check_status_{order_id}")]
        ]
        await query.edit_message_caption(caption=text_invoice, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await query.edit_message_caption(caption="⚠️ Failed to generate payment link. Please try again later.")

