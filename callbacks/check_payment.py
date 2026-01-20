import db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from duitku_api import DuitkuAPI

PATTERN = "^check_status_"
dui = DuitkuAPI()

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Checking payment status...")

    # Data format: check_status_{order_id}
    order_id = query.data.split('_', 2)[2]
    
    order = db.get_order(order_id)
    if not order:
        await query.edit_message_caption(caption="⚠️ Order not found.")
        return

    # Unpack order details (order_id, user_id, product_name, amount, status, payment_url, payment_ref)
    _, user_id, product_name, amount, status, payment_url, payment_ref = order

    if status == 'SUCCESS':
        await query.edit_message_caption(caption=f"✅ <b>PAYMENT SUCCESSFUL!</b>\n\nProduct: {product_name}\n\n<i>Use /accounts to view your account.</i>", parse_mode='HTML')
        return

    # Check via API
    result = dui.check_transaction_status(order_id)
    
    if result and result.get("statusCode") == "00":  # 00 is usually success in Duitku
        # Update DB
        db.update_order_status(order_id, 'SUCCESS')
        
        # Delivery Logic (simplified)
        account = db.get_random_account(product_name)
        
        if account:
            acc_id, email, username, password = account
            # Send account details to user
            try:
                msg = (
                    f"✅ <b>PAYMENT RECEIVED!</b>\n"
                    f"Here is your account:\n\n"
                    f"📧 Email: <code>{email}</code>\n"
                    f"👤 User: <code>{username}</code>\n"
                    f"🔑 Pass: <code>{password}</code>\n\n"
                    f"<i>Thank you for purchasing!</i>"
                )
                await context.bot.send_message(chat_id=user_id, text=msg, parse_mode='HTML')
                
                # Update DB (Delete sold account)
                db.delete_account(acc_id)
                
                await query.edit_message_caption(caption=f"✅ <b>PAYMENT SUCCESSFUL!</b>\n\nAccount has been sent to your DM.", parse_mode='HTML')
                
            except Exception as e:
                print(f"Failed to send account: {e}")
                await query.edit_message_caption(caption=f"✅ <b>PAYMENT SUCCESSFUL!</b>\n\nFailed to send DM. Please contact admin.", parse_mode='HTML')

        else:
             await query.edit_message_caption(caption=f"✅ <b>PAYMENT SUCCESSFUL!</b>\n\n⚠️ Stock empty. Please contact admin.", parse_mode='HTML')
            
    else:
        status_desc = result.get("statusMessage", "Pending") if result else "Unknown"
        
        text_invoice = (
            f"<b>⏳ PAYMENT PENDING</b>\n\n"
            f"📌 <b>Order ID:</b> <code>{order_id}</code>\n"
            f"📦 <b>Kategori:</b> {product_name.upper()}\n"
            f"💰 <b>Total Bayar:</b> Rp {amount:,}\n"
            f"ℹ️ <b>Status:</b> {status_desc}\n\n"
            f"<i>Please complete payment via the link below.</i>"
        )
        
        keyboard = [
            [InlineKeyboardButton("🔗 Pay Now", url=payment_url)],
            [InlineKeyboardButton("🔄 Check Status", callback_data=f"check_status_{order_id}")]
        ]
        await query.edit_message_caption(caption=text_invoice, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
