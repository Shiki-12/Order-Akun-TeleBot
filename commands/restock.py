from telegram import Update
from telegram.ext import ContextTypes
import db
from config import RESTOCK_ALLOWED

DESCRIPTION = "Add account: /restock <email> <user> <pass> [owner only]"

async def restock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in RESTOCK_ALLOWED:
        await update.message.reply_text("You don't have permission to use this command.")
        return

    
    if update.message.document:
        document = update.message.document
        file_name = document.file_name
        
        if not file_name.lower().endswith('.csv'):
             await update.message.reply_text("❌ Please upload a valid CSV file.")
             return

        # Download file
        new_file = await context.bot.get_file(document.file_id)
        from io import StringIO
        import csv
        
        # Download file to memory
        file_content = await new_file.download_as_bytearray()
        decoded_content = file_content.decode('utf-8')
        
        csv_file = StringIO(decoded_content)
        reader = csv.DictReader(csv_file)
        
        success_count = 0
        error_count = 0
        errors = []
        
        # Check if headers exist
        required_headers = {'email', 'username', 'password', 'category'}
        if not reader.fieldnames or not required_headers.issubset(set(reader.fieldnames)):
             await update.message.reply_text(f"❌ Invalid CSV Format. Headers must be: {', '.join(required_headers)}")
             return

        for row in reader:
            try:
                db.add_account(row['email'], row['username'], row['password'], row['category'])
                success_count += 1
            except Exception as e:
                error_count += 1
                errors.append(f"{row.get('username', 'Unknown')}: {str(e)}")
        
        msg = f"<b>✅ Restock CSV Completed</b>\n\nSuccessful: {success_count}\nFailed: {error_count}"
        if errors:
            msg += "\n\nErrors:\n" + "\n".join(errors[:10]) # Limit errors display
            
        await update.message.reply_text(msg, parse_mode='HTML')
        return

    # Safe access to args
    args = context.args if context.args is not None else []

    # Existing logic for arguments
    if len(args) != 4:
        await update.message.reply_text(
            "<b>❌ Format Salah!</b>\n\n"
            "Cara 1: Upload file CSV dengan caption <code>/restock</code>\n"
            "Cara 2: <code>/restock [email] [username] [password] [category]</code>\n"
            "Contoh: <code>/restock user@mail.com username pass123 Netflix</code>",
            parse_mode='HTML'
        )
        return
    
    email = args[0]
    username = args[1]
    password = args[2]
    category = args[3]

    try:
        db.add_account(email, username, password, category)
        await update.message.reply_text(f"Account saved for **{username}** in **{category}**!", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Database error: {e}")

# Define handlers explicitly
from telegram.ext import CommandHandler, MessageHandler, filters
HANDLERS = [
    CommandHandler("restock", restock_command),
    MessageHandler(filters.Document.ALL & filters.CaptionRegex(r"^/restock"), restock_command)
]