from inventory_service import add_product, delete_product, get_products


def test_delete_product_removes_existing_item(db_path):
    add_product("Mouse", 8, 19.5, "Electronics", db_path)
    products = get_products(db_path)
    product_id = products[0][0]

    delete_product(product_id, db_path)

    assert get_products(db_path) == []
