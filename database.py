import sqlite3

"""Creates and returns a connection to the SQLite database."""
def get_connection():
    return sqlite3.connect("inventory.db")

"""Creates the products table if it does not exist."""
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            category TEXT
        )
    """)

    conn.commit()
    conn.close()