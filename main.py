"""
Inventory System - GUI Version
Main entry point using Tkinter.
"""

import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk, messagebox

import inventory_service as service
from database import create_table
import validators

# INIT DATABASE

# Ensure the database and table exist before starting the app.
create_table()


# MAIN WINDOW

# Create the main Tkinter window and set the initial application layout.

root = tk.Tk()
root.title("Inventory System")
root.geometry("980x650")
root.minsize(980, 650)
root.configure(bg="#f4f7fb")

# FRAMES (LAYOUT STRUCTURE)

top_frame = tk.Frame(root, bg="#f4f7fb")
top_frame.pack(fill="x", padx=20, pady=15)

button_frame = tk.Frame(root, bg="#f4f7fb")
button_frame.pack(fill="x", padx=20, pady=(0, 12))

table_frame = tk.Frame(root, bg="#ffffff", bd=1, relief="solid")
table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# INPUT VARIABLES

# Input variable for search functionality
search_var = tk.StringVar()
category_filter_var = tk.StringVar(value="")

tk.Label(top_frame, text="Search", bg="#f4f7fb", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, padx=(0, 8), pady=8)
search_entry = tk.Entry(top_frame, textvariable=search_var, width=30, font=("Segoe UI", 10))
search_entry.grid(row=2, column=1, padx=(0, 12), pady=8)

tk.Label(top_frame, text="Category", bg="#f4f7fb", font=("Segoe UI", 10, "bold")).grid(row=2, column=2, padx=(0, 8), pady=8)
category_entry = tk.Entry(top_frame, textvariable=category_filter_var, width=20, font=("Segoe UI", 10))
category_entry.grid(row=2, column=3, padx=(0, 12), pady=8)

# These variables store user input from the GUI fields
name_var = tk.StringVar()
qty_var = tk.StringVar()
price_var = tk.StringVar()
category_var = tk.StringVar()

# FUNCTIONS

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

def add_product():
    """
    Collect data from the form and save a new product.
    """
    # Validate the form values before inserting the product into the database.

    name = name_var.get()
    qty = qty_var.get()
    price = price_var.get()
    category = category_var.get()

    # VALIDATION STEP
    if not validate_inputs(name, qty, price, category):
        return

    # SAFE CONVERSION (after validation)
    service.add_product(
        name,
        int(qty),
        float(price),
        category
    )

    messagebox.showinfo("Success", "Product added successfully")

    clear_fields()
    load_products()
    reset_search()

def update_product():
    # Update the stock quantity of the currently selected product.
    selected = table.focus()

    if not selected:
        messagebox.showwarning("Warning", "No product selected")
        return

    data = table.item(selected)['values']
    new_qty = simpledialog.askstring("Update Stock", "Enter new quantity:")

    if not new_qty or not new_qty.isdigit():
        messagebox.showerror("Invalid Input", "Quantity must be a number")
        return

    service.update_stock(data[0], int(new_qty))
    messagebox.showinfo("Updated", "Stock updated successfully")
    load_products()
    refresh_summary()
    if search_var.get():
        search_products()


def edit_selected_product():
    # Open a small dialog to edit the selected product details.
    selected = table.focus()

    if not selected:
        messagebox.showwarning("Warning", "No product selected")
        return

    data = table.item(selected)['values']
    dialog = tk.Toplevel(root)
    dialog.title("Edit Product")
    dialog.geometry("380x260")
    dialog.transient(root)

    name_edit = tk.StringVar(value=data[1])
    qty_edit = tk.StringVar(value=str(data[2]))
    price_edit = tk.StringVar(value=str(data[3]))
    category_edit = tk.StringVar(value=data[4])

    tk.Label(dialog, text="Name").grid(row=0, column=0, padx=10, pady=8, sticky="w")
    tk.Entry(dialog, textvariable=name_edit).grid(row=0, column=1, padx=10, pady=8)

    tk.Label(dialog, text="Qty").grid(row=1, column=0, padx=10, pady=8, sticky="w")
    tk.Entry(dialog, textvariable=qty_edit).grid(row=1, column=1, padx=10, pady=8)

    tk.Label(dialog, text="Price").grid(row=2, column=0, padx=10, pady=8, sticky="w")
    tk.Entry(dialog, textvariable=price_edit).grid(row=2, column=1, padx=10, pady=8)

    tk.Label(dialog, text="Category").grid(row=3, column=0, padx=10, pady=8, sticky="w")
    tk.Entry(dialog, textvariable=category_edit).grid(row=3, column=1, padx=10, pady=8)

    def save_edit():
        try:
            if not validate_inputs(name_edit.get(), qty_edit.get(), price_edit.get(), category_edit.get()):
                return
            service.update_product(
                data[0],
                name_edit.get().strip(),
                int(qty_edit.get()),
                float(price_edit.get()),
                category_edit.get().strip(),
            )
            messagebox.showinfo("Updated", "Product updated successfully")
            dialog.destroy()
            load_products()
            refresh_summary()
            if search_var.get():
                search_products()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid values")

    ttk.Button(dialog, text="Save", command=save_edit).grid(row=4, column=0, columnspan=2, pady=12)

def delete_product():
    """
    Delete the selected product from the table and database.
    """
    # Remove the current selection after confirmation.
    selected = table.focus()

    if not selected:
        messagebox.showwarning("Warning", "No product selected")
        return

    data = table.item(selected)['values']
    service.delete_product(data[0])
    messagebox.showinfo("Deleted", "Product removed")
    load_products()
    if search_var.get():
        search_products()

def load_products():
    # Reload the product list from the database into the Treeview table.
    for row in table.get_children():
        table.delete(row)

    for product in service.get_products():
        table.insert("", "end", values=product)


def refresh_summary():
    # Refresh the inventory summary shown in the UI footer.
    summary = service.get_summary()
    summary_var.set(
        f"Products: {summary['products']} | Total qty: {summary['quantity']} | Total value: ${summary['value']:.2f}"
    )


def clear_fields():
    """
    Clear all input fields after adding a product.
    """
    # Reset the form fields so the user can enter a new product quickly.
    name_var.set("")
    qty_var.set("")
    price_var.set("")
    category_var.set("")

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

# INPUT FIELDS (UI)

header_label = tk.Label(top_frame, text="Inventory Management", bg="#f4f7fb", font=("Segoe UI", 18, "bold"), fg="#1f2937")
header_label.grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 12))

product_card = tk.LabelFrame(top_frame, text="Product form", bg="#ffffff", padx=12, pady=10, font=("Segoe UI", 10, "bold"))
product_card.grid(row=1, column=0, columnspan=6, sticky="ew", pady=(0, 8))

# Product name input
tk.Label(product_card, text="Name", bg="#ffffff").grid(row=0, column=0, padx=(0, 8), pady=4)
tk.Entry(product_card, textvariable=name_var, width=24, font=("Segoe UI", 10)).grid(row=0, column=1, padx=(0, 12), pady=4)

# Quantity input
tk.Label(product_card, text="Qty", bg="#ffffff").grid(row=0, column=2, padx=(0, 8), pady=4)
tk.Entry(product_card, textvariable=qty_var, width=12, font=("Segoe UI", 10)).grid(row=0, column=3, padx=(0, 12), pady=4)

# Price input
tk.Label(product_card, text="Price", bg="#ffffff").grid(row=1, column=0, padx=(0, 8), pady=4)
tk.Entry(product_card, textvariable=price_var, width=24, font=("Segoe UI", 10)).grid(row=1, column=1, padx=(0, 12), pady=4)

# Category input
tk.Label(product_card, text="Category", bg="#ffffff").grid(row=1, column=2, padx=(0, 8), pady=4)
tk.Entry(product_card, textvariable=category_var, width=12, font=("Segoe UI", 10)).grid(row=1, column=3, padx=(0, 12), pady=4)

# TABLE FRAME WITH SCROLL

table_container = tk.Frame(table_frame, bg="#ffffff")
table_container.pack(fill="both", expand=True, padx=12, pady=12)

scrollbar = tk.Scrollbar(table_container)
scrollbar.pack(side="right", fill="y")

table = ttk.Treeview(
    table_container,
    columns=("ID", "Name", "Qty", "Price", "Category"),
    show="headings",
    yscrollcommand=scrollbar.set
)

scrollbar.config(command=table.yview)

for col in ("ID", "Name", "Qty", "Price", "Category"):
    table.heading(col, text=col, command=lambda c=col: sort_table(c))

table.pack(fill="both", expand=True)

# BUTTONS

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 10), padding=(10, 6))
style.configure("Accent.TButton", background="#2563eb", foreground="white")
style.map("Accent.TButton", background=[("active", "#1d4ed8")])

btn_add = ttk.Button(button_frame, text="Add", style="Accent.TButton", command=add_product)
btn_add.pack(side="left", padx=5)
ttk.Button(button_frame, text="Update stock", command=update_product).pack(side="left", padx=5)
ttk.Button(button_frame, text="Edit", command=edit_selected_product).pack(side="left", padx=5)
ttk.Button(button_frame, text="Delete", command=delete_product).pack(side="left", padx=5)
ttk.Button(button_frame, text="Search", command=search_products).pack(side="left", padx=5)
ttk.Button(button_frame, text="Reset", command=reset_search).pack(side="left", padx=5)

# INITIAL LOAD

# Load data when app starts
load_products()

# STATUS BAR
status_var = tk.StringVar(value="Ready")
summary_var = tk.StringVar(value="")
status_bar = tk.Label(root, textvariable=status_var, bg="#e2e8f0", fg="#0f172a", anchor="w", padx=12, pady=6)
status_bar.pack(fill="x", side="bottom")

summary_label = tk.Label(root, textvariable=summary_var, bg="#f4f7fb", fg="#334155", padx=20, pady=(8, 0), anchor="w")
summary_label.pack(fill="x")

# RUN APP

refresh_summary()
root.mainloop()