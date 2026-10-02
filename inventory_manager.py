# Inventory Management System (INF1103 Lab 5)
# Each product is a dictionary. All products are kept in one list.

LINE = "-" * 48


# ---------- Input helpers ----------

def get_text(prompt):
    """Ask again until the user types some text."""
    while True:
        text = input(prompt).strip()
        if text != "":
            return text
        print("This field cannot be empty.")


def get_price(prompt):
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
    product_id = get_text("Product ID: ").upper()
    if find_product(inventory, product_id) is not None:
        print(f"{product_id} already exists.")
        return

    name = get_text("Product Name: ")
    price = get_price("Price: ")
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


# ---------- Main program ----------

def show_menu():
    # Options 3, 4 and 5 come in the next commits.
    print()
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    # Start with 3 products. Each product is a dictionary in the list.
    inventory = [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15, "history": [15]},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40, "history": [40]},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25, "history": [25]},
    ]

    while True:
        show_menu()
        choice = input("Enter option: ").strip()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "6":
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Enter 1, 2 or 6.")


main()