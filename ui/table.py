import inventory_service as service

_sort_states = {}

def load_products(table, service_module=service):
    """Load all products from the database into a Treeview widget."""
    # Clear any existing rows before inserting the latest product list.
    for row in table.get_children():
        table.delete(row)

    # Insert each product record into the table view.
    for product in service_module.get_products():
        table.insert("", "end", values=product)


def refresh_summary(summary_var, service_module=service):
    """Refresh the inventory summary shown in the UI."""
    # Read the current totals and format them for the summary label.
    summary = service_module.get_summary()
    summary_var.set(
        f"Products: {summary['products']} | "
        f"Total qty: {summary['quantity']} | "
        f"Total value: ${summary['value']:.2f}"
    )


def search_products(table, search_var, category_filter_var, service_module=service):
    """Filter products by name and category."""
    # Read the current search terms and apply them to the product list.
    query = search_var.get().lower()
    category = category_filter_var.get().strip()

    # Remove any previously displayed rows before showing filtered results.
    for row in table.get_children():
        table.delete(row)

    products = service_module.get_products()
    filtered = [p for p in products if query in str(p[1]).lower()]

    if category:
        filtered = [p for p in filtered if str(p[4]).lower() == category.lower()]

    # Show the filtered product rows in the table.
    for product in filtered:
        table.insert("", "end", values=product)


def reset_search(table, search_var, category_filter_var, service_module=service):
    """Clear search filters and show all products again."""
    # Reset the input fields and reload the complete product list.
    search_var.set("")
    category_filter_var.set("")
    load_products(table, service_module)


def sort_table(table, column):

    reverse = _sort_states.get(column, False)
    """Sort the table data by the selected column."""
    # Collect the current visible rows and sort them by the requested column.
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

    # Clear the existing rows and display the sorted data.
    for item in table.get_children():
        table.delete(item)

    for row in data:
        table.insert("", "end", values=row)

    _sort_states[column] = not reverse

    arrow = "▼" if not reverse else "▲"

    columns = ["ID", "Name", "Qty", "Price", "Category"]

    for col in columns:
        text = col

        if col == column:
            text = f"{col} {arrow}"

        table.heading(
            col,
            text=text,
            command=lambda c=col: sort_table(table, c)
        )
