def search_products():
    """
    Filter products by name and category.
    """
    # Refresh the inventory table based on the current search and category filters.

    query = search_var.get().lower()
    category = category_filter_var.get().strip()

    for row in table.get_children():
        table.delete(row)

    products = service.get_products()
    filtered = [p for p in products if query in str(p[1]).lower()]

    if category:
        filtered = [p for p in filtered if str(p[4]).lower() == category.lower()]

    for product in filtered:
        table.insert("", "end", values=product)

def reset_search():
    """
    Reset the filters and show all products again.
    """
    # Restore the full product list and clear the active filters.
    search_var.set("")
    category_filter_var.set("")
    load_products()

def sort_table(column, reverse=False):
    """
    Sort the table data by the selected column.
    """
    # Rebuild the displayed rows in the requested sort order.

    data = [(table.item(item)["values"]) for item in table.get_children()]

    col_index = {
        "ID": 0,
        "Name": 1,
        "Qty": 2,
        "Price": 3,
        "Category": 4,
    }[column]

    try:
        data.sort(
            key=lambda x: float(x[col_index]) if column in ["Qty", "Price"] else str(x[col_index]).lower(),
            reverse=reverse,
        )
    except ValueError:
        data.sort(key=lambda x: str(x[col_index]).lower(), reverse=reverse)

    for item in table.get_children():
        table.delete(item)

    for row in data:
        table.insert("", "end", values=row)

    table.heading("ID", text="ID", command=lambda: sort_table("ID"))
    table.heading("Name", text="Name", command=lambda: sort_table("Name"))
    table.heading("Qty", text="Qty", command=lambda: sort_table("Qty"))
    table.heading("Price", text="Price", command=lambda: sort_table("Price"))
    table.heading("Category", text="Category", command=lambda: sort_table("Category"))

def load_products():
    # Reload the product list from the database into the Treeview table.
    for row in table.get_children():
        table.delete(row)

    for product in service.get_products():
        table.insert("", "end", values=product)
