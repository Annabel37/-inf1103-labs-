# File handling (INF1103 Lab 6)
# Responsibility: load and save inventory.json.
# Product and Inventory do not know about the file.

import json
import os

from product import Product
from inventory import Inventory

FILE_NAME = "inventory.json"


def load_inventory():
    """Load inventory.json into an Inventory object."""
    inventory = Inventory()

    if not os.path.exists(FILE_NAME):
        print(f"{FILE_NAME} not found.")
        print("Starting with an empty inventory.")
        return inventory

    print(f"{FILE_NAME} found.")
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
        for item in data:
            product = Product(item["id"], item["name"], item["price"],
                              item["stock"], item.get("history"))
            inventory.add_product(product)
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        print(f"{FILE_NAME} is damaged. Starting with an empty inventory.")
        return Inventory()

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    """Write all products to inventory.json (same format as Week 5)."""
    data = []
    for product in inventory.get_products():
        data.append({
            "id": product.get_product_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
            "history": product.get_history(),
        })
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)