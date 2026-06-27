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