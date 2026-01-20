import sqlite3
import time

DB_NAME = "accounts.db"



def add_account(email, username, password, category):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO accounts (email, username, password, category) VALUES (?, ?, ?, ?)', 
                   (email, username, password, category.lower()))
    conn.commit()
    conn.close()

def get_all_accounts():
    """Returns a list of all accounts."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT email, username, password, category FROM accounts')
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
    """Mengambil daftar nama produk, kategori dan jumlah stoknya."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT username, category, COUNT(*) FROM accounts GROUP BY username, category')
    rows = cursor.fetchall()
    conn.close()
    return rows

def setup_db():
    """Creates the table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tabel akun (stok)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            username TEXT,
            password TEXT,
            category TEXT
        )
    ''')
    
    # Simple migration: Add category column if it doesn't exist
    try:
        cursor.execute('ALTER TABLE accounts ADD COLUMN category TEXT')
    except sqlite3.OperationalError:
        pass # Column likely already exists

    # Tabel kategori (harga & deskripsi)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            name TEXT PRIMARY KEY,
            price INTEGER,
            description TEXT
        )
    ''')
    # Tabel orders
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            user_id INTEGER,
            product_name TEXT,
            amount INTEGER,
            status TEXT DEFAULT 'PENDING',
            created_at INTEGER,
            payment_url TEXT,
            payment_ref TEXT
        )
    ''')
    
    # Migration: Add payment_url and payment_ref if they don't exist
    try:
        cursor.execute('ALTER TABLE orders ADD COLUMN payment_url TEXT')
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute('ALTER TABLE orders ADD COLUMN payment_ref TEXT')
    except sqlite3.OperationalError:
        pass

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

def create_order(order_id, user_id, product_name, amount, payment_url=None, payment_ref=None):
    """Mencatat pesanan baru ke database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (order_id, user_id, product_name, amount, created_at, payment_url, payment_ref)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (order_id, user_id, product_name, amount, int(time.time()), payment_url, payment_ref))
    conn.commit()
    conn.close()

def get_unique_categories():
    """Mengambil daftar kategori dan jumlah stoknya."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Filter only accounts that have a category set
    cursor.execute('SELECT category, COUNT(*) FROM accounts WHERE category IS NOT NULL AND category != "" GROUP BY category')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_random_account(category):
    """Mengambil satu akun random berdasarkan kategori."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, username, password FROM accounts WHERE category = ? ORDER BY RANDOM() LIMIT 1', (category,))
    row = cursor.fetchone()
    conn.close()
    return row

def delete_account(account_id):
    """Menghapus akun setelah terjual."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM accounts WHERE id = ?', (account_id,))
    conn.commit()
    conn.close()

def get_order(order_id):
    """Mengambil detail pesanan."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT order_id, user_id, product_name, amount, status, payment_url, payment_ref FROM orders WHERE order_id = ?', (order_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_order_status(order_id, status):
    """Update status pesanan."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE orders SET status = ? WHERE order_id = ?', (status, order_id))
    conn.commit()
    conn.close()

  