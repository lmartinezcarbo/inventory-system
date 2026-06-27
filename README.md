# 📦 Inventory System (GUI Version)

A desktop inventory management system built with Python, Tkinter, and SQLite.

---

## 🧠 Description

This project is a GUI-based inventory system that supports full CRUD operations for products. It uses a small modular architecture with separate files for the database layer, business logic, and the user interface.

---

## ✨ Features

- Add new products
- View all products in a table
- Update stock quantity
- Edit product details
- Delete products
- Search by product name
- Filter by category
- View an inventory summary
- Store data in SQLite
- Use a Tkinter-based graphical interface

---

## 🏗️ Project Structure

```
InventorySystem/
│
├── main.py                  # GUI application (Tkinter)
├── database.py              # SQLite connection and table setup
├── inventory_service.py     # CRUD logic and summary helpers
├── tests/test_inventory.py  # Regression tests for CRUD operations
├── requirements.txt         # Project dependencies
└── inventory.db             # Database file (generated automatically)
```

---

## 🚀 How to Run

```bash
python main.py
```

---

## 🗄️ Database

The system uses SQLite. The database file is created automatically when the app runs.

### Table schema

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    category TEXT
);
```

---

## ✅ Validation

You can verify the CRUD flow with:

```bash
python -m unittest discover -s tests -v
```

---

## 📌 Notes

- Tkinter and sqlite3 are included with most Python installations.
- No external package is required for this project.

---

## 👨‍💻 Author

Built for learning purposes.