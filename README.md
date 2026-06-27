# 📦 Inventory System (GUI Version)

A desktop inventory management system built with Python, Tkinter, and SQLite.

---

## 🧠 Description

This project is a GUI-based inventory system that supports product management with CRUD operations, search, category filtering, stock updates, editing, and a summary view. The application is organized in small modules for the database layer, business logic, UI, and validation.

---

## ✨ Features

- Add new products
- View all products in a table
- Update stock quantity
- Edit existing product details
- Delete products
- Search by product name
- Filter by category
- View an inventory summary
- Persist data in SQLite
- Use a Tkinter-based graphical interface
- Validate input before saving changes

---

## 🏗️ Project Structure

```text
inventory-system/
├── main.py                  # Application entry point
├── database.py              # SQLite connection and table creation
├── inventory_service.py     # CRUD and summary logic
├── validators.py            # Input validation helpers
├── pytest.ini               # Pytest configuration
├── requirements.txt         # Project dependencies
├── tests/                   # Test suite for CRUD and summary flows
│   ├── conftest.py
│   ├── test_add_product.py
│   ├── test_delete_product.py
│   ├── test_update_product.py
│   └── test_summary.py
├── ui/                      # Tkinter UI modules
│   ├── dialogs.py
│   ├── main_window.py
│   └── table.py
└── inventory.db             # SQLite database file (created automatically)
```

---

## 🚀 How to Run

Run the app with:

```bash
python main.py
```

---

## 🧪 Running Tests

The project uses pytest for automated tests.

Install pytest if needed:

```bash
pip install -r requirements.txt
```

Then run:

```bash
pytest -q
```

---

## 🗄️ Database

The system uses SQLite. The database file is created automatically when the app starts.

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

## 📌 Notes

- Tkinter and sqlite3 are included with most Python installations.
- No external GUI framework is required.
- The app is intended for learning and small-scale inventory management.

---

## 👨‍💻 Author

Built for learning purposes.