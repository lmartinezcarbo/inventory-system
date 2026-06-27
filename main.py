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

# Run application
root.mainloop()


# INPUT VARIABLES

# These variables store user input from the GUI fields
name_var = tk.StringVar()
qty_var = tk.StringVar()
price_var = tk.StringVar()
category_var = tk.StringVar()

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