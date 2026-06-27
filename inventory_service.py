from pathlib import Path
from typing import Optional

from database import get_connection

"""Insert a new product into the inventory."""
def add_product(name, quantity, price, category, db_path: Optional[str | Path] = None):
    # Save a new product record into the database.
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products (name, quantity, price, category)
        VALUES (?, ?, ?, ?)
    """, (name, quantity, price, category))

    conn.commit()
    conn.close()

"""Return all products from the database."""
def get_products(db_path: Optional[str | Path] = None):
    # Load every product row from the database.
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()

    conn.close()
    return data

"""Delete a product by its ID."""
def delete_product(product_id, db_path: Optional[str | Path] = None):
    # Remove the selected product from storage.
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))

    conn.commit()
    conn.close()

"""Update the stock quantity of a product."""
def update_stock(product_id, quantity, db_path: Optional[str | Path] = None):
    # Update only the stock field for the selected product.
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET quantity = ?
        WHERE id = ?
    """, (quantity, product_id))

    conn.commit()
    conn.close()

"""Update all editable fields of a product."""
def update_product(product_id, name, quantity, price, category, db_path: Optional[str | Path] = None):
    # Replace the editable product details for the selected record.
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET name = ?, quantity = ?, price = ?, category = ?
        WHERE id = ?
    """, (name, quantity, price, category, product_id))

    conn.commit()
    conn.close()

"""Return inventory summary values."""
def get_summary(db_path: Optional[str | Path] = None):
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

"""Return products filtered by category."""
def get_products_by_category(category, db_path: Optional[str | Path] = None):
    # Retrieve only products that belong to the requested category.
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE LOWER(category) = LOWER(?)", (category,))
    data = cursor.fetchall()

    conn.close()
    return data