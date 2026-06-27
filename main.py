from database import create_table
import inventory_service as service
from utils import print_products

create_table()

def menu():
    print("\n--- INVENTORY SYSTEM ---")
    print("1. Add product")
    print("2. View products")
    print("3. Delete product")
    print("4. Update stock")
    print("5. Exit")

def main():
    # Ensure database and table exist
    create_table()

    while True:
        # Show menu options to the user
        menu()
        option = input("Choose: ")

        # Add new product
        if option == "1":
            name = input("Name: ")
            qty = int(input("Quantity: "))
            price = float(input("Price: "))
            category = input("Category: ")

            service.add_product(name, qty, price, category)

        # View all products
        elif option == "2":
            products = service.get_products()
            print_products(products)

        # Delete a product
        elif option == "3":
            pid = int(input("Product ID: "))
            service.delete_product(pid)
        # Update stock quantity of a product
        elif option == "4":
            pid = int(input("Product ID: "))
            qty = int(input("New quantity: "))
            service.update_stock(pid, qty)

        elif option == "5":
            print("Goodbye!")
            break

main()