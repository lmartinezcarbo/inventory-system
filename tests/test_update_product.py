from inventory_service import add_product, get_products, update_product


def test_update_product_changes_existing_item(db_path):
    add_product("Monitor", 3, 199.99, "Electronics", db_path)
    product_id = get_products(db_path)[0][0]

    update_product(product_id, "Monitor 27 inch", 4, 249.99, "Displays", db_path)

    updated = get_products(db_path)[0]
    assert updated[1] == "Monitor 27 inch"
    assert updated[2] == 4
    assert updated[3] == 249.99
    assert updated[4] == "Displays"
