
# Responsibility: load and save inventory.json.
import os
import json
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from inventory import Inventory

class FileHandler:
    
    def __init__(self, file_name: str = "inventory.json"):
        # Saves the filename as an instance variable (matched to self.file_name)
        self.file_name = file_name

    def create_product(self, item):
        """Make the correct product object from one saved record.
        Return None if the type is missing or unknown."""
        product_type = item.get("type")

        if product_type == "physical":
            return PhysicalProduct(
                item["id"], item["name"], item["price"],
                item["stock"], item["weight"], item.get("history")
            )
        if product_type == "digital":
            return DigitalProduct(
                item["id"], item["name"], item["price"],
                item["stock"], item["download_size"], item.get("history")
            )
        return None

    def load_inventory(self):
        """Load inventory from file into an Inventory object."""
        inventory = Inventory()

        if not os.path.exists(self.file_name):
            print(f"{self.file_name} not found.")
            print("Starting with an empty inventory.")
            return inventory

        print(f"{self.file_name} found.")
        try:
            with open(self.file_name, "r") as file:
                data = json.load(file)
            for item in data:
                product = self.create_product(item)
                if product is None:
                    print(f"Skipped {item.get('id', '?')}: the product type is missing or unknown.")
                    continue
                inventory.add_product(product)
        except (json.JSONDecodeError, KeyError, ValueError, TypeError):
            print(f"{self.file_name} is damaged. Starting with an empty inventory.")
            return Inventory()

        print("Inventory loaded successfully.")
        return inventory

    def save_inventory(self, inventory):
        """Write all products to file, with the type and the extra value."""
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

        with open(self.file_name, "w") as file:
            json.dump(data, file, indent=4)