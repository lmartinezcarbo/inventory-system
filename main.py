"""
Inventory System - GUI Version
Main entry point using Tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import inventory_service as service
from database import create_table


# INIT DATABASE

# Ensure the database and table exist before starting the app
create_table()


# MAIN WINDOW

root = tk.Tk()
root.title("Inventory System")
root.geometry("700x500")

# INPUT VARIABLES

# These variables store user input from the GUI fields
name_var = tk.StringVar()
qty_var = tk.StringVar()
price_var = tk.StringVar()
category_var = tk.StringVar()

# FUNCTIONS

def add_product():
    """
    Collect data from inputs and send it to service layer.
    """
    name = name_var.get()
    qty = int(qty_var.get())
    price = float(price_var.get())
    category = category_var.get()

    service.add_product(name, qty, price, category)

    messagebox.showinfo("Success", "Product added successfully")

    clear_fields()
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
tk.Label(root, text="Name").pack()
tk.Entry(root, textvariable=name_var).pack()

# Quantity input
tk.Label(root, text="Quantity").pack()
tk.Entry(root, textvariable=qty_var).pack()

# Price input
tk.Label(root, text="Price").pack()
tk.Entry(root, textvariable=price_var).pack()

# Category input
tk.Label(root, text="Category").pack()
tk.Entry(root, textvariable=category_var).pack()

# PRODUCT TABLE

# Treeview widget to display all products
table = ttk.Treeview(
    root,
    columns=("ID", "Name", "Qty", "Price", "Category"),
    show="headings"
)

# Define table headers
table.heading("ID", text="ID")
table.heading("Name", text="Name")
table.heading("Qty", text="Qty")
table.heading("Price", text="Price")
table.heading("Category", text="Category")

table.pack(fill="both", expand=True)

# BUTTONS

tk.Button(root, text="Add Product", command=add_product).pack(pady=5)
tk.Button(root, text="Delete Selected", command=delete_product).pack(pady=5)


# INITIAL LOAD

# Load data when app starts
load_products()


# RUN APP

root.mainloop()