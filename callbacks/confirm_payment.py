import db
from telegram import Update
from telegram.ext import ContextTypes

PATTERN = "^confirm_"

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    order_id = query.data.split('_')[1]
    order = db.get_order(order_id)
    
    if not order:
        await query.edit_message_caption(caption="❌ Order tidak ditemukan.", parse_mode='HTML')
        return

    # order: (order_id, user_id, product_name, amount, status)
    status = order[4]
    category = order[2]
    
    if status == 'COMPLETED':
        await query.edit_message_caption(
            caption=f"✅ <b>Order {order_id} sudah selesai!</b>\nAkun telah dikirim sebelumnya.",
            parse_mode='HTML'
        )
        return

    # Fulfillment logic
    account = db.get_random_account(category)
    
    if account:
        # account: (id, email, username, password)
        account_id, email, username, password = account
        
        # Mark as sold (delete) and update order
        db.delete_account(account_id)
        db.update_order_status(order_id, 'COMPLETED')
        
        message = (
            f"✅ <b>PEMBAYARAN BERHASIL!</b>\n\n"
            f"📦 <b>Kategori:</b> {category.upper()}\n"
            f"🆔 <b>Order ID:</b> <code>{order_id}</code>\n\n"
            f"🔐 <b>AKUN ANDA:</b>\n"
            f"📧 <b>Email:</b> <code>{email}</code>\n"
            f"👤 <b>Username:</b> <code>{username}</code>\n"
            f"🔑 <b>Password:</b> <code>{password}</code>\n\n"
            f"<i>Terima kasih telah berbelanja!</i>"
        )
        await query.edit_message_caption(caption=message, parse_mode='HTML')
    else:
        await query.edit_message_caption(
            caption=f"❌ <b>Stok Habis!</b>\nMaaf, stok untuk kategori <b>{category}</b> baru saja habis.", 
            parse_mode='HTML'
        )
