from inventory_service import add_product, get_products


def test_add_product_saves_new_item(db_path):
    add_product("Keyboard", 5, 49.99, "Electronics", db_path)

    products = get_products(db_path)

    assert len(products) == 1
    assert products[0][1] == "Keyboard"
    assert products[0][2] == 5
    assert products[0][3] == 49.99
    assert products[0][4] == "Electronics"
