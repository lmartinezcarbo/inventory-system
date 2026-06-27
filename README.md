# 📦 Inventory System (GUI Version)

A desktop inventory management system built with Python, Tkinter, and SQLite.

---

## 🧠 Description

This project is a GUI-based inventory system that allows users to manage products using full CRUD operations (Create, Read, Update, Delete). It uses a modular architecture separating database logic, business logic, and UI.

---

## ✨ Features

- Add new products
- View all products in a table
- Update product stock
- Delete products
- SQLite database storage
- Tkinter graphical interface
- Modular code structure

---

## 🏗️ Project Structure

```
InventorySystem/
│
├── main.py                # GUI application (Tkinter)
├── database.py            # SQLite connection and table setup
├── inventory_service.py   # Business logic (CRUD operations)
├── utils.py               # Helper functions
├── requirements.txt       # Project dependencies
└── inventory.db           # Database file (auto-generated)
```

---

## 🚀 How to Run

```bash
python main.py
```

---

## 🗄️ Database

The system uses SQLite. The database file is created automatically when the app runs.

### Table schema:

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

## 📌 Learning Goals

- Python OOP and modular design
- GUI development with Tkinter
- CRUD operations
- SQLite database handling
- Software architecture basics

---

## 📈 Future Improvements

- Improve UI design (modern layout)
- Add product search feature
- Add filters (category, stock level)
- Export data to CSV
- Add authentication system

---

## 👨‍💻 Author

Built for learning purposes.