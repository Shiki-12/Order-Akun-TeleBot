from telegram import Update
from telegram.ext import ContextTypes
from commands.accounts import get_stock_message
from commands.help import get_help_message
import config

PATTERN = "^(check_stock|help|add_balance|my_account|voucher)$"

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "check_stock":
        text = get_stock_message()
        await query.edit_message_caption(caption=text, parse_mode='HTML', reply_markup=None) # Or keep back button logic if we want nested menus

    elif data == "help":
        commands = context.bot_data.get("command_list", [])
        user_id = update.effective_user.id
        text = get_help_message(commands, user_id)
        await query.edit_message_caption(caption=text, parse_mode='HTML', reply_markup=None)

    elif data == "add_balance":
        await query.edit_message_caption(caption="💰 <b>Isi Saldo</b>\n\nFitur ini sedang dalam pengembangan. Silakan hubungi admin untuk topup manual.", parse_mode='HTML')

    elif data == "my_account":
        user = update.effective_user
        # Re-using the logic from start command (simplified)
        text = (
            f"👤 <b>Akun Saya</b>\n\n"
            f"Nama: {user.first_name}\n"
            f"Username: @{user.username if user.username else 'None'}\n"
            f"ID: <code>{user.id}</code>\n"
        )
        await query.edit_message_caption(caption=text, parse_mode='HTML')

    elif data == "voucher":
        await query.edit_message_caption(caption="🎟️ <b>Voucher</b>\n\nBelum ada voucher yang tersedia saat ini.", parse_mode='HTML')
