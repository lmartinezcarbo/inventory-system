"""
Inventory System - GUI Version
Main entry point using Tkinter.
"""

import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk, messagebox

import inventory_service as service
from database import create_table


# INIT DATABASE

# Ensure the database and table exist before starting the app
create_table()


# MAIN WINDOW

root = tk.Tk()
root.title("Inventory System")
root.geometry("800x500")
root.minsize(800, 500)

# FRAMES (LAYOUT STRUCTURE)

top_frame = tk.Frame(root)
top_frame.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True)

root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# INPUT VARIABLES

# Input variable for search functionality
search_var = tk.StringVar()

tk.Label(top_frame, text="Search").grid(row=2, column=0)
tk.Entry(top_frame, textvariable=search_var).grid(row=2, column=1)

# These variables store user input from the GUI fields
name_var = tk.StringVar()
qty_var = tk.StringVar()
price_var = tk.StringVar()
category_var = tk.StringVar()

# FUNCTIONS

def search_products():
    """
    Filter products by name.
    """

    query = search_var.get().lower()

    # clear table
    for row in table.get_children():
        table.delete(row)

    # get all products
    products = service.get_products()

    # filter locally
    filtered = [
        p for p in products
        if query in str(p[1]).lower()
    ]

    for product in filtered:
        table.insert("", "end", values=product)

def reset_search():
    """
    Reset table to show all products.
    """
    search_var.set("")
    load_products()

def add_product():
    """
    Collect data from inputs and send it to service layer.
    """

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

def update_product():
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

def delete_product():
    """
    Delete selected product from table and database.
    """
    selected = table.focus()

    if not selected:
        messagebox.showwarning("Warning", "No product selected")
        return

    data = table.item(selected)['values']
    service.delete_product(data[0])

    messagebox.showinfo("Deleted", "Product removed")
    load_products()

def load_products():
    for row in table.get_children():
        table.delete(row)

    for product in service.get_products():
        table.insert("", "end", values=product)


def clear_fields():
    """
    Clear all input fields after adding a product.
    """
    name_var.set("")
    qty_var.set("")
    price_var.set("")
    category_var.set("")

# INPUT FIELDS (UI)

# Product name input
tk.Label(top_frame, text="Name").grid(row=0, column=0)
tk.Entry(top_frame, textvariable=name_var).grid(row=0, column=1)

# Quantity input
tk.Label(top_frame, text="Qty").grid(row=0, column=2)
tk.Entry(top_frame, textvariable=qty_var).grid(row=0, column=3)

# Price input
tk.Label(top_frame, text="Price").grid(row=1, column=0)
tk.Entry(top_frame, textvariable=price_var).grid(row=1, column=1)

# Category input
tk.Label(top_frame, text="Category").grid(row=1, column=2)
tk.Entry(top_frame, textvariable=category_var).grid(row=1, column=3)

# TABLE FRAME WITH SCROLL

table_container = tk.Frame(table_frame)
table_container.pack(fill="both", expand=True)

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
    table.heading(col, text=col)

table.pack(fill="both", expand=True)

# BUTTONS

tk.Button(button_frame, text="Add", command=add_product).pack(side="left", padx=5)
tk.Button(button_frame, text="Update", command=update_product).pack(side="left", padx=5)
tk.Button(button_frame, text="Delete", command=delete_product).pack(side="left", padx=5)
tk.Button(button_frame, text="Search", command=search_products).pack(side="left", padx=5)
tk.Button(button_frame, text="Reset", command=reset_search).pack(side="left", padx=5)

# INITIAL LOAD

# Load data when app starts
load_products()


def validate_inputs(name, qty, price, category):
    """
    Validates user input before inserting into database.
    """

    # NAME must be letters only
    if not name.replace(" ", "").isalpha():
        messagebox.showerror("Invalid Input", "Name must contain only letters")
        return False

    # CATEGORY must be letters only
    if not category.replace(" ", "").isalpha():
        messagebox.showerror("Invalid Input", "Category must contain only letters")
        return False

    # QUANTITY must be number (int)
    if not qty.isdigit():
        messagebox.showerror("Invalid Input", "Quantity must be a number")
        return False

    # PRICE must be number (float safe check)
    try:
        float(price)
    except ValueError:
        messagebox.showerror("Invalid Input", "Price must be a valid number")
        return False

    return True

# RUN APP

root.mainloop()