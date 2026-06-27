import sqlite3
from pathlib import Path
from typing import Optional

# Default database file used by the inventory application.
DEFAULT_DB_PATH = Path(__file__).with_name("inventory.db")


def get_connection(db_path: Optional[str | Path] = None):
    """Create and return a connection to the SQLite database."""
    # Build the database path and ensure the parent directory exists.
    db_file = Path(db_path or DEFAULT_DB_PATH)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_file)


def create_table(db_path: Optional[str | Path] = None):
    """Create the products table if it does not exist."""
    # Open a connection and ensure the required table structure is available.
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            category TEXT
        )
        """
    )

    conn.commit()
    conn.close()