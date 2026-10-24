# Inventory Management System - OOP version (INF1103 Lab 6)
# Main program responsibility: show the menu, get user input,
# and call the correct Inventory methods.

from product import Product
from file_handler import load_inventory, save_inventory, FILE_NAME

LINE = "-" * 48


# ---------- Input helpers ----------

def input_text(prompt):
    """Ask again until the user types some text."""
    while True:
        text = input(prompt).strip()
        if text != "":
            return text
        print("This field cannot be empty.")


def input_price(prompt):
    """Ask again until the user types a price of 0 or more."""
    while True:
        try:
            price = float(input(prompt))
            if price >= 0:
                return price
            print("The price cannot be less than 0.")
        except ValueError:
            print("Type a number, for example 25.50.")


def input_quantity(prompt):
    """Ask again until the user types a whole number of 0 or more."""
    while True:
        try:
            quantity = int(input(prompt))
            if quantity >= 0:
                return quantity
            print("The quantity cannot be less than 0.")
        except ValueError:
            print("Type a whole number, for example 10.")


# ---------- Menu actions ----------

def add_product(inventory):
    print("Add New Product")
    product_id = input_text("Product ID: ").upper()
    if inventory.search_product(product_id) is not None:
        print(f"{product_id} already exists. Use option 3 to update its stock.")
        return

    name = input_text("Product Name: ")
    price = input_price("Price: ")
    stock = input_quantity("Stock Quantity: ")

    product = Product(product_id, name, price, stock)
    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory):
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    new_stock = input_quantity("New Stock Quantity: ")

    change = product.update_stock(new_stock)   # the Product changes its own stock
    if change == 0:
        print("The stock is the same. No change made.")
    else:
        print("Stock updated successfully!")


def search_product(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print(LINE)
    product.display_information()
    print(LINE)


def show_menu():
    print()
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


# ---------- Main program ----------

def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    while True:
        show_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("Saving inventory...")
            save_inventory(inventory)
            print(f"Inventory saved successfully to {FILE_NAME}.")
        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Enter a number from 1 to 6.")


if __name__ == "__main__":
    main()