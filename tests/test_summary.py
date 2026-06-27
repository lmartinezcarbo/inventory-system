from inventory_service import add_product, get_summary


def test_summary_returns_total_products_quantity_and_value(db_path):
    add_product("Laptop", 2, 1000.0, "Computers", db_path)
    add_product("Phone", 3, 500.0, "Electronics", db_path)

    summary = get_summary(db_path)

    assert summary["products"] == 2
    assert summary["quantity"] == 5
    assert summary["value"] == 3500.0
