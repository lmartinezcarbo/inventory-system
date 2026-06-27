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
