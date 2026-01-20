import sqlite3
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

DB_NAME = "accounts.db"
KEY = os.getenv("ENCRYPTION_KEY")

if not KEY:
    print("Error: ENCRYPTION_KEY not found in .env")
    exit(1)

cipher = Fernet(KEY)

def encrypt_password(password):
    if not password:
        return ""
    # Ensure bytes
    if isinstance(password, str):
        password = password.encode()
    return cipher.encrypt(password).decode()

def migrate():
    print("Starting migration...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Get all accounts
    cursor.execute('SELECT id, password FROM accounts')
    accounts = cursor.fetchall()
    
    updated_count = 0
    
    for acc_id, password in accounts:
        # Check if already encrypted (Fernet tokens start with gAAAA...)
        # A simple heuristic: if it doesn't look like a fernet token, encrypt it.
        # Or just encrypt everything if we assume strict migration from plaintext.
        # Let's try to detect if it's already encrypted to be safe, 
        # but standard Fernet tokens are long urlsafe base64 strings.
        # If the password is "password123", it's short.
        # Encryption results are usually long.
        
        try:
            # Try to decrypt. If successful, it's already encrypted.
            cipher.decrypt(password.encode())
            print(f"Skipping account {acc_id}: Already encrypted.")
            continue
        except Exception:
            # Not encrypted (or invalid), so we encrypt it.
            pass
            
        encrypted = encrypt_password(password)
        cursor.execute('UPDATE accounts SET password = ? WHERE id = ?', (encrypted, acc_id))
        updated_count += 1
        
    conn.commit()
    conn.close()
    print(f"Migration finished. Encrypted {updated_count} accounts.")

if __name__ == "__main__":
    migrate()
