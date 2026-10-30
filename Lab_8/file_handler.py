# File handling (INF1103 Lab 8)
# Responsibility: load and save inventory.json.
# Product and Inventory do not know about the file.

import json
import os

from product import PhysicalProduct, DigitalProduct
from inventory import Inventory

FILE_NAME = "inventory.json"


def create_product(item):
    """Make the correct product object from one saved record.
    Return None if the type is missing or unknown."""
    product_type = item.get("type")

    if product_type == "physical":
        return PhysicalProduct(item["id"], item["name"], item["price"],
                               item["stock"], item["weight"], item.get("history"))
    if product_type == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"],
                              item["stock"], item["download_size"], item.get("history"))
    return None


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
            product = create_product(item)
            if product is None:
                print(f"Skipped {item.get('id', '?')}: the product type is missing or unknown.")
                continue
            inventory.add_product(product)
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        print(f"{FILE_NAME} is damaged. Starting with an empty inventory.")
        return Inventory()

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    """Write all products to inventory.json, with the type and the extra value."""
    data = []
    for product in inventory.get_products():
        record = {
            "id": product.get_product_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
            "history": product.get_history(),
        }

        # Save the type and the extra value, so that load can make the correct class.
        if isinstance(product, PhysicalProduct):
            record["type"] = "physical"
            record["weight"] = product.get_weight()
        elif isinstance(product, DigitalProduct):
            record["type"] = "digital"
            record["download_size"] = product.get_download_size()

        data.append(record)

    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)