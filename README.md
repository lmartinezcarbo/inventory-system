# 📦 Inventory System

A modular inventory management system built with Python and SQLite for managing products, stock, and categories.

---

## 🧠 Description

This project is a command-line inventory system that allows users to manage products using CRUD operations. It is built with a modular architecture to separate database, business logic, and utility functions.

---

## ✨ Features

- Add new products
- View all products
- Update stock quantity
- Delete products
- SQLite database storage
- Modular project structure

---

## 🏗️ Project Structure

```
InventorySystem/
│
├── main.py                # Entry point of the application
├── database.py            # SQLite connection and table creation
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

The project uses SQLite.  
The database file (`inventory.db`) is created automatically when the program runs.

Table structure:

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

This project was built to practice:

- Python modular programming
- CRUD operations
- SQLite database handling
- Clean code organization

---

## 📈 Future Improvements

- Add GUI with Tkinter
- Add product search feature
- Add stock alerts (low inventory)
- Export data to CSV
- Convert to REST API (FastAPI)

---

## 👨‍💻 Author

Created for learning purposes.