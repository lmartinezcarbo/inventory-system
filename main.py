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
root.geometry("700x500")

# FRAMES (LAYOUT STRUCTURE)

top_frame = tk.Frame(root)
top_frame.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True)

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

def update_product():
    """
    Update selected product quantity in database.
    """
    selected = table.focus()

    if not selected:
        messagebox.showwarning("Warning", "No product selected")
        return

    data = table.item(selected)['values']

    new_qty = simpledialog.askinteger("Update Stock", "Enter new quantity:")

    if new_qty is None:
        return

    service.update_stock(data[0], new_qty)

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

# PRODUCT TABLE

# Treeview widget to display all products
table = ttk.Treeview(
    table_frame,
    columns=("ID", "Name", "Qty", "Price", "Category"),
    show="headings"
)

for col in ("ID", "Name", "Qty", "Price", "Category"):
    table.heading(col, text=col)

table.pack(fill="both", expand=True)

# BUTTONS

tk.Button(button_frame, text="Add", command=add_product).pack(side="left", padx=5)
tk.Button(button_frame, text="Update", command=update_product).pack(side="left", padx=5)
tk.Button(button_frame, text="Delete", command=delete_product).pack(side="left", padx=5)

# INITIAL LOAD

# Load data when app starts
load_products()


# RUN APP

root.mainloop()