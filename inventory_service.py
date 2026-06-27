import sqlite3

from pathlib import Path
from typing import Optional

from database import get_connection


def add_product(name, quantity, price, category, db_path: Optional[str | Path] = None):
    """Insert a new product into the inventory."""

    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO products (name, quantity, price, category)
            VALUES (?, ?, ?, ?)
            """,
            (name, quantity, price, category),
        )

        conn.commit()

    except sqlite3.Error as e:
        raise RuntimeError(f"Database error: {e}")

    finally:
        conn.close()


def get_products(db_path: Optional[str | Path] = None):
    """Return all products from the database."""

    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM products")
            return cursor.fetchall()

    except sqlite3.Error as e:
        raise RuntimeError(f"Database error: {e}")


def delete_product(product_id, db_path: Optional[str | Path] = None):
    """Delete a product by its ID."""
    # Remove the selected product from storage.
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))

    conn.commit()
    conn.close()


def update_stock(product_id, quantity, db_path: Optional[str | Path] = None):
    """Update the stock quantity of a product."""
    # Update only the stock field for the selected product.
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE products
        SET quantity = ?
        WHERE id = ?
        """,
        (quantity, product_id),
    )

    conn.commit()
    conn.close()


def update_product(product_id, name, quantity, price, category, db_path: Optional[str | Path] = None):
    """Update all editable fields of a product."""
    # Replace the editable product details for the selected record.
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE products
        SET name = ?, quantity = ?, price = ?, category = ?
        WHERE id = ?
        """,
        (name, quantity, price, category, product_id),
    )

    conn.commit()
    conn.close()


def get_summary(db_path: Optional[str | Path] = None):
    """Return inventory summary values."""
    # Calculate the total number of products, units, and stock value.
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*), COALESCE(SUM(quantity), 0), COALESCE(SUM(price * quantity), 0) FROM products")
    count, total_quantity, total_value = cursor.fetchone()

    conn.close()
    return {
        "products": count,
        "quantity": total_quantity,
        "value": total_value,
    }


def get_products_by_category(category, db_path: Optional[str | Path] = None):
    """Return products filtered by category."""
    # Retrieve only products that belong to the requested category.
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE LOWER(category) = LOWER(?)", (category,))
    data = cursor.fetchall()

    conn.close()
    return data