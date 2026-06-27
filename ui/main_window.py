import tkinter as tk
from tkinter import ttk, messagebox

import inventory_service as service
from database import create_table
from ui.dialogs import edit_selected_product, update_product as update_stock_dialog
from ui.table import load_products, refresh_summary, search_products, reset_search, sort_table
from validators import validate_product_data

class MainWindow:
    """Create and manage the Tkinter inventory window."""

    def __init__(self):
        # Create the main application window and initialize its state.
        self.root = tk.Tk()
        self.root.title("Inventory System")
        self.root.geometry("980x650")
        self.root.minsize(980, 650)
        self.root.configure(bg="#f4f7fb")

        # Store the input and display variables used by the form and summary area.
        self.search_var = tk.StringVar()
        self.category_filter_var = tk.StringVar(value="")
        self.name_var = tk.StringVar()
        self.qty_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.summary_var = tk.StringVar(value="")

        # Build the UI, create the database table, and load the initial product data.
        self.create_layout()
        self.create_table()
        self.create_buttons()
        self.load_initial_data()

    def create_layout(self):
        # Build the top toolbar, form area, and product table container.
        self.top_frame = tk.Frame(self.root, bg="#f4f7fb")
        self.top_frame.pack(fill="x", padx=20, pady=15)

        self.button_frame = tk.Frame(self.root, bg="#f4f7fb")
        self.button_frame.pack(fill="x", padx=20, pady=(0, 12))

        self.table_frame = tk.Frame(self.root, bg="#ffffff", bd=1, relief="solid")
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Add search and category filter controls at the top of the window.
        tk.Label(self.top_frame, text="Search", bg="#f4f7fb", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, padx=(0, 8), pady=8)
        self.search_entry = tk.Entry(self.top_frame, textvariable=self.search_var, width=30, font=("Segoe UI", 10))
        self.search_entry.grid(row=2, column=1, padx=(0, 12), pady=8)

        tk.Label(self.top_frame, text="Category", bg="#f4f7fb", font=("Segoe UI", 10, "bold")).grid(row=2, column=2, padx=(0, 8), pady=8)
        self.category_entry = tk.Entry(self.top_frame, textvariable=self.category_filter_var, width=20, font=("Segoe UI", 10))
        self.category_entry.grid(row=2, column=3, padx=(0, 12), pady=8)

        # Add the main title and the product entry form.
        tk.Label(self.top_frame, text="Inventory Management", bg="#f4f7fb", font=("Segoe UI", 18, "bold"), fg="#1f2937").grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 12))

        self.product_card = tk.LabelFrame(self.top_frame, text="Product form", bg="#ffffff", padx=12, pady=10, font=("Segoe UI", 10, "bold"))
        self.product_card.grid(row=1, column=0, columnspan=6, sticky="ew", pady=(0, 8))

        tk.Label(self.product_card, text="Name", bg="#ffffff").grid(row=0, column=0, padx=(0, 8), pady=4)
        tk.Entry(self.product_card, textvariable=self.name_var, width=24, font=("Segoe UI", 10)).grid(row=0, column=1, padx=(0, 12), pady=4)

        tk.Label(self.product_card, text="Qty", bg="#ffffff").grid(row=0, column=2, padx=(0, 8), pady=4)
        tk.Entry(self.product_card, textvariable=self.qty_var, width=12, font=("Segoe UI", 10)).grid(row=0, column=3, padx=(0, 12), pady=4)

        tk.Label(self.product_card, text="Price", bg="#ffffff").grid(row=1, column=0, padx=(0, 8), pady=4)
        tk.Entry(self.product_card, textvariable=self.price_var, width=24, font=("Segoe UI", 10)).grid(row=1, column=1, padx=(0, 12), pady=4)

        tk.Label(self.product_card, text="Category", bg="#ffffff").grid(row=1, column=2, padx=(0, 8), pady=4)
        tk.Entry(self.product_card, textvariable=self.category_var, width=12, font=("Segoe UI", 10)).grid(row=1, column=3, padx=(0, 12), pady=4)

        # Build the treeview container and add the product table.
        self.table_container = tk.Frame(self.table_frame, bg="#ffffff")
        self.table_container.pack(fill="both", expand=True, padx=12, pady=12)

        self.scrollbar = tk.Scrollbar(self.table_container)
        self.scrollbar.pack(side="right", fill="y")

        self.table = ttk.Treeview(
            self.table_container,
            columns=("ID", "Name", "Qty", "Price", "Category"),
            show="headings",
            yscrollcommand=self.scrollbar.set,
        )
        self.scrollbar.config(command=self.table.yview)

        for col in ("ID", "Name", "Qty", "Price", "Category"):
            self.table.heading(col, text=col, command=lambda c=col: sort_table(self.table, c))

        self.table.pack(fill="both", expand=True)

        # Display the status bar and inventory summary at the bottom of the window.
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bg="#e2e8f0", fg="#0f172a", anchor="w", padx=12, pady=6)
        self.status_bar.pack(fill="x", side="bottom")

        self.summary_label = tk.Label(self.root, textvariable=self.summary_var, bg="#f4f7fb", fg="#334155", padx=20, pady=8, anchor="w")
        self.summary_label.pack(fill="x")

    def create_table(self):
        # Ensure the SQLite table exists before the application starts using it.
        create_table()

    def create_buttons(self):
        # Style the action buttons and connect them to the appropriate handlers.
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=(10, 6))
        style.configure("Accent.TButton", background="#2563eb", foreground="white")
        style.map("Accent.TButton", background=[("active", "#1d4ed8")])

        ttk.Button(self.button_frame, text="Add", style="Accent.TButton", command=self.add_product).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Update stock", command=lambda: update_stock_dialog(self.table, self.root, self)).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Edit", command=lambda: edit_selected_product(self.table, self.root, self)).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Delete", command=self.delete_product).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Search", command=self.search_products).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Reset", command=self.reset_search).pack(side="left", padx=5)

    def validate_inputs(self, name, qty, price, category):
        valid, message = validate_product_data(
        name,
        qty,
        price,
        category,
    )

        if not valid:
            messagebox.showerror(
            "Invalid Input",
            message,
        )

        return valid

    def add_product(self):
        # Read the form values and save a new product if the input is valid.
        name = self.name_var.get()
        qty = self.qty_var.get()
        price = self.price_var.get()
        category = self.category_var.get()

        if not self.validate_inputs(name, qty, price, category):
            return

        service.add_product(name, int(qty), float(price), category)
        messagebox.showinfo("Success", "Product added successfully")
        self.clear_fields()
        load_products(self.table)
        self.reset_search()
        self.refresh_summary()

    def delete_product(self):
        # Remove the selected product from the database and refresh the UI.
        selected = self.table.focus()
        if not selected:
            messagebox.showwarning("Warning", "No product selected")
            return

        data = self.table.item(selected)["values"]
        confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete '{data[1]}'?"
        )

        if not confirm:
            return        
        service.delete_product(data[0])
        messagebox.showinfo("Deleted", "Product removed")
        load_products(self.table)
        self.refresh_summary()
        if self.search_var.get():
            self.search_products()

    def clear_fields(self):
        # Reset the form fields after a successful add action.
        self.name_var.set("")
        self.qty_var.set("")
        self.price_var.set("")
        self.category_var.set("")

    def search_products(self):
        # Apply the search filters to the visible table rows.
        search_products(self.table, self.search_var, self.category_filter_var)

    def reset_search(self):
        # Restore the full list and clear the active filters.
        reset_search(self.table, self.search_var, self.category_filter_var)

    def refresh_summary(self):
        # Update the summary label with the latest inventory totals.
        refresh_summary(self.summary_var)

    def load_initial_data(self):
        # Load the existing products when the application starts.
        load_products(self.table)
        self.refresh_summary()


def main():
    # Create the database table and launch the Tkinter window.
    create_table()
    window = MainWindow()
    window.root.mainloop()


if __name__ == "__main__":
    main()
