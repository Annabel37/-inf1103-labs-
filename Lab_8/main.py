# Inventory Management System - OOP version (INF1103 Lab 6)
# Main program responsibility: show the menu, get user input,
# and call the correct Inventory methods.

#from product import PhysicalProduct, DigitalProduct
from supplier import Supplier
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from inventory import Inventory
from order import Order
from product import Product

LINE = "-" * 48


# ---------- Input helpers ----------

# def input_text(prompt):
#     """Ask again until the user types some text."""
#     while True:
#         text = input(prompt).strip()
#         if text != "":
#             return text
#         print("This field cannot be empty.")


# def input_price(prompt):
#     """Ask again until the user types a price of 0 or more."""
#     while True:
#         try:
#             price = float(input(prompt))
#             if price >= 0:
#                 return price
#             print("The price cannot be less than 0.")
#         except ValueError:
#             print("Type a number, for example 25.50.")


# def input_quantity(prompt):
#     """Ask again until the user types a whole number of 0 or more."""
#     while True:
#         try:
#             quantity = int(input(prompt))
#             if quantity >= 0:
#                 return quantity
#             print("The quantity cannot be less than 0.")
#         except ValueError:
#             print("Type a whole number, for example 10.")


# def input_size(prompt):
#     """Ask again until the user types a number of more than 0 (weight or download size)."""
#     while True:
#         try:
#             value = float(input(prompt))
#             if value > 0:
#                 return value
#             print("The value must be more than 0.")
#         except ValueError:
#             print("Type a number, for example 1.5.")


# def input_product_type():
#     """Ask again until the user types 1 (physical) or 2 (digital)."""
#     while True:
#         print("Product Type:")
#         print("1. Physical Product")
#         print("2. Digital Product")
#         choice = input("Enter type: ").strip()
#         if choice in ("1", "2"):
#             return choice
#         print("Invalid type. Enter 1 or 2.")


# # ---------- Menu actions ----------

# def add_product(inventory):
#     print("Add New Product")
#     product_id = input_text("Product ID: ").upper()
#     if inventory.search_product(product_id) is not None:
#         print(f"{product_id} already exists. Use option 3 to update its stock.")
#         return

#     product_type = input_product_type()
#     name = input_text("Product Name: ")
#     price = input_price("Price: ")
#     stock = input_quantity("Stock Quantity: ")

#     # Ask for the extra value that this product type needs.
#     if product_type == "1":
#         weight = input_size("Weight (kg): ")
#         product = PhysicalProduct(product_id, name, price, stock, weight)
#     else:
#         download_size = input_size("Download Size (MB): ")
#         product = DigitalProduct(product_id, name, price, stock, download_size)

#     inventory.add_product(product)
#     print("Product added successfully!")


# def update_stock(inventory):
#     print("Update Stock")
#     product_id = input("Enter Product ID: ").strip().upper()
#     product = inventory.search_product(product_id)
#     if product is None:
#         print("Product not found.")
#         return

#     print("Product Found:")
#     print(f"Name: {product.get_name()}")
#     print(f"Current Stock: {product.get_stock()}")
#     new_stock = input_quantity("New Stock Quantity: ")

#     change = product.update_stock(new_stock)   # the Product changes its own stock
#     if change == 0:
#         print("The stock is the same. No change made.")
#     else:
#         print("Stock updated successfully!")


# def search_product(inventory):
#     print("Search Product")
#     product_id = input("Enter Product ID: ").strip().upper()
#     product = inventory.search_product(product_id)
#     if product is None:
#         print("Product not found.")
#         return

#     print("Product Found")
#     print(LINE)
#     product.display_information()
#     print(f"Fulfilment: {product.get_fulfilment_info()}")
#     print(LINE)


# def show_menu():
#     print()
#     print("----------- MENU -----------")
#     print("1. Display All Products")
#     print("2. Add Product")
#     print("3. Update Stock")
#     print("4. Search Product")
#     print("5. Save Inventory")
#     print("6. Exit")
#     print("----------------------------")


# # ---------- Main program ----------

# def main():
#     print("=" * 40)
#     print("INVENTORY MANAGEMENT SYSTEM")
#     print("=" * 40)

#     inventory = load_inventory()

#     while True:
#         show_menu()
#         choice = input("Enter option: ").strip()

#         if choice == "1":
#             inventory.display_all()
#         elif choice == "2":
#             add_product(inventory)
#         elif choice == "3":
#             update_stock(inventory)
#         elif choice == "4":
#             search_product(inventory)
#         elif choice == "5":
#             print("Saving inventory...")
#             save_inventory(inventory)
#             print(f"Inventory saved successfully to {FILE_NAME}.")
#         elif choice == "6":
#             print("Saving inventory before exit...")
#             save_inventory(inventory)
#             print("Inventory saved successfully.")
#             print("Thank you for using Inventory Management System.")
#             print("Program terminated.")
#             break
#         else:
#             print("Invalid option. Enter a number from 1 to 6.")


# if __name__ == "__main__":
#     main()

# Inventory Management System - OOP version (INF1103 Lab 8)
# Main program responsibility: show the menu, get user input,
# and call the correct Inventory and Order methods.

from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from supplier import Supplier
from order import Order
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


def input_size(prompt):
    """Ask again until the user types a number of more than 0 (weight or download size)."""
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("The value must be more than 0.")
        except ValueError:
            print("Type a number, for example 1.5.")


def input_product_type():
    """Ask again until the user types 1 (physical) or 2 (digital)."""
    while True:
        print("Product Type:")
        print("1. Physical Product")
        print("2. Digital Product")
        choice = input("Enter type: ").strip()
        if choice in ("1", "2"):
            return choice
        print("Invalid type. Enter 1 or 2.")


# ---------- Menu actions ----------

def add_product(inventory):
    print("Add New Product")
    product_id = input_text("Product ID: ").upper()
    if inventory.search_product(product_id) is not None:
        print(f"{product_id} already exists. Use option 3 to update its stock.")
        return

    product_type = input_product_type()
    name = input_text("Product Name: ")
    price = input_price("Price: ")
    stock = input_quantity("Stock Quantity: ")

    # Lab 8 Association: Ask for Supplier details
    print("--- Supplier Information ---")
    supp_id = input_text("Supplier ID: ").upper()
    supp_name = input_text("Supplier Name: ")
    supp_email = input_text("Supplier Contact Email: ")
    supplier = Supplier(supp_id, supp_name, supp_email)

    # Ask for the extra value that this product type needs.
    if product_type == "1":
        weight = input_size("Weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, weight, supplier)
    else:
        download_size = input_size("Download Size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, download_size, supplier)

    inventory.add_product(product)
    print("Product added successfully with Supplier association!")


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
    product.display_information() # Polymorphic call + Supplier info
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    print(LINE)


def test_order_composition(inventory):
    """Demonstrates Composition (Order & OrderLine) using products from inventory."""
    print("Test Order Composition")
    if not inventory.get_products():
        print("Inventory is empty! Add some products first.")
        return

    order_id = input_text("Enter Order ID: ").upper()
    order = Order(order_id)

    while True:
        prod_id = input("Enter Product ID to add to order (or type 'done' to finish): ").strip().upper()
        if prod_id == 'DONE':
            break
        
        product = inventory.search_product(prod_id)
        if product is None:
            print("Product not found in inventory.")
            continue
        
        qty = input_quantity("Enter Quantity: ")
        order.add_order_line(product, qty)
        print(f"Added {qty}x {product.get_name()} to order.")

    print(LINE)
    print(f"Order Summary for {order.order_id}:")
    for line in order.order_lines:
        print(f" - {line.product.get_name()} x {line.quantity} @ ${line.product.get_price():.2f} = ${line.calculate_subtotal():.2f}")
    print(f"Total Order Value: ${order.calculate_total():.2f}")
    print(LINE)


def show_menu():
    print()
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product (with Supplier)")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Create Test Order (Composition)")
    print("6. Save Inventory")
    print("7. Exit")
    print("----------------------------")


# ---------- Main program ----------

def main():
    print("=" * 48)
    print("INVENTORY MANAGEMENT SYSTEM (LAB 8)")
    print("=" * 48)

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
            test_order_composition(inventory)
        elif choice == "6":
            print("Saving inventory...")
            save_inventory(inventory)
            print(f"Inventory saved successfully to {FILE_NAME}.")
        elif choice == "7":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Enter a number from 1 to 7.")


if __name__ == "__main__":
    main()

