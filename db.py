import sqlite3
import time

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

def get_total_accounts_count():
    import sqlite3
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM accounts')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_unique_products():
    """Mengambil daftar nama produk dan jumlah stoknya."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT username, COUNT(*) FROM accounts GROUP BY username')
    rows = cursor.fetchall()
    conn.close()
    return rows

def setup_db():
    """Membuat tabel jika belum ada."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tabel akun (stok)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            username TEXT,
            password TEXT
        )
    ''')
    # Tabel kategori (harga & deskripsi)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            name TEXT PRIMARY KEY,
            price INTEGER,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def set_product_price(name, price, description=""):
    """Menyimpan atau mengupdate harga produk."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Menggunakan INSERT OR REPLACE agar jika nama produk sudah ada, harganya terupdate
    cursor.execute('''
        INSERT OR REPLACE INTO categories (name, price, description) 
        VALUES (?, ?, ?)
    ''', (name.lower(), price, description))
    conn.commit()
    conn.close()

def get_product_details(name):
    """Mengambil detail harga dan deskripsi produk."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT price, description FROM categories WHERE name = ?', (name.lower(),))
    row = cursor.fetchone()
    conn.close()
    return row if row else (0, "Deskripsi belum diatur.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            user_id INTEGER,
            product_name TEXT,
            amount INTEGER,
            status TEXT DEFAULT 'PENDING',
            created_at INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def create_order(order_id, user_id, product_name, amount):
    """Mencatat pesanan baru ke database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (order_id, user_id, product_name, amount, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (order_id, user_id, product_name, amount, int(time.time())))
    conn.commit()
    conn.close()

  