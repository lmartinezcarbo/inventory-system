import sqlite3
from pathlib import Path
from typing import Optional

DEFAULT_DB_PATH = Path(__file__).with_name("inventory.db")

"""Create and return a connection to the SQLite database."""
def get_connection(db_path: Optional[str | Path] = None):
    # Open a SQLite connection for the inventory database file.
    db_file = Path(db_path or DEFAULT_DB_PATH)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_file)

"""Create the products table if it does not exist."""
def create_table(db_path: Optional[str | Path] = None):
    # Ensure the table structure exists before using the app.
    conn = get_connection(db_path)
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