import sqlite3

DB_NAME = "accounts.db"

def setup_db():
    """Creates the table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            username TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_account(email, username, password):
    """Saves a new account."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO accounts (email, username, password) VALUES (?, ?, ?)', 
                   (email, username, password))
    conn.commit()
    conn.close()

def get_all_accounts():
    """Returns a list of all accounts."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT email, username, password FROM accounts')
    rows = cursor.fetchall()
    conn.close()
    return rows