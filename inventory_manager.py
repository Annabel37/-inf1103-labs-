# Inventory Management System (INF1103 Lab 5)
# Each product is a dictionary. All products are kept in one list.
# The list is saved in inventory.json, so the data stays after the program closes.

import json
import os

FILE_NAME = "inventory.json"
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
                return round(price, 2)
            print("The price cannot be less than 0.")
        except ValueError:
            print("Type a number, for example 25.50.")


def get_quantity(prompt):
    """Ask again until the user types a whole number of 0 or more."""
    while True:
        try:
            quantity = int(input(prompt))
            if quantity >= 0:
                return quantity
            print("The quantity cannot be less than 0.")
        except ValueError:
            print("Type a whole number, for example 10.")


def find_product(inventory, product_id):
    """Return the product with this ID. Return None if it is not in the list."""
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None


# ---------- File functions ----------

def load_inventory():
    """Load inventory.json if it exists. If not, start with an empty list."""
    if not os.path.exists(FILE_NAME):
        print(f"{FILE_NAME} not found.")
        print("Starting with an empty inventory.")
        return []

    print(f"{FILE_NAME} found.")
    try:
        with open(FILE_NAME, "r") as file:
            inventory = json.load(file)
    except json.JSONDecodeError:
        print(f"{FILE_NAME} is damaged. Starting with an empty inventory.")
        return []

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    """Write the full product list to inventory.json."""
    with open(FILE_NAME, "w") as file:
        json.dump(inventory, file, indent=4)


# ---------- Menu functions ----------

def display_all(inventory):
    """Show each product on one line."""
    print("Current Inventory")
    print(LINE)
    if len(inventory) == 0:
        print("The inventory is empty.")
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | "
              f"Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print(LINE)


def add_product(inventory):
    """Ask for a new product and add it to the list."""
    print("Add New Product")
    product_id = input_text("Product ID: ").upper()
    if find_product(inventory, product_id) is not None:
        print(f"{product_id} already exists. Use option 3 to update its stock.")
        return

    name = input_text("Product Name: ")
    price = input_price("Price: ")
    stock = get_quantity("Stock Quantity: ")

    # The start stock is the first transaction in the history.
    product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
        "history": [stock],
    }
    inventory.append(product)
    print("Product added successfully!")


def update_stock(inventory):
    """Set a new stock quantity. Keep the change in the history list."""
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = find_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    new_stock = get_quantity("New Stock Quantity: ")

    change = new_stock - product["stock"]   # transaction amount, for example +10 or -5
    if change == 0:
        print("The stock is the same. No change made.")
        return

    product["stock"] = new_stock            # running total
    product["history"].append(change)       # every transaction amount
    print("Stock updated successfully!")


def search_product(inventory):
    """Find one product by its ID and show its details."""
    print("Search Product")
    product_id = input("Enter Product ID: ").strip().upper()
    product = find_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print(LINE)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print(f"History: {product['history']}")
    print(LINE)


# ---------- Main program ----------

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


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    while True:
        show_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            display_all(inventory)
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


main()