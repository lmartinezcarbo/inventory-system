from database import get_connection

def add_product(name, quantity, price, category):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products (name, quantity, price, category)
        VALUES (?, ?, ?, ?)
    """, (name, quantity, price, category))

    conn.commit()
    conn.close()


def get_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()

    conn.close()
    return data
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))

    conn.commit()
    conn.close()


def update_stock(product_id, quantity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET quantity = ?
        WHERE id = ?
    """, (quantity, product_id))

    conn.commit()
    conn.close()