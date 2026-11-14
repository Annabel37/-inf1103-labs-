# Responsibility: load and save inventory.json and products.csv.
import csv
import json
import os
from digitalproduct import DigitalProduct
from inventory import Inventory
from physicalproduct import PhysicalProduct
from ProductFactory import ProductFactory


class FileHandler:

  def __init__(self, file_name: str = "inventory.json"):
    self.file_name = file_name

  def load_inventory(self):
    """Load inventory from json file into an Inventory object."""
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
        # Recreating products from json storage
        product_type = item.get("type")
        if product_type == "physical":
          product = ProductFactory.create(
              product_type,
              item["id"],
              item["name"],
              item["price"],
              item["stock"],
              None,  # Adjust supplier if stored in your JSON
              weight=item.get("weight", 1.0),
          )
        elif product_type == "digital":
          product = ProductFactory.create(
              product_type,
              item["id"],
              item["name"],
              item["price"],
              item["stock"],
              None,
              download_size=item.get("download_size", 10.0),
          )
        else:
          print(
              f"Skipped {item.get('id', '?')}: the product type is missing or"
              " unknown."
          )
          continue
        inventory.add_product(product)
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
      print(f"{self.file_name} is damaged. Starting with an empty inventory.")
      return Inventory()

    print("Inventory loaded successfully.")
    return inventory

  def save_inventory(self, inventory):
    """Write all products to json file."""
    data = []
    for product in inventory.get_products():
      record = {
          "id": product.get_product_id(),
          "name": product.get_name(),
          "price": product.get_price(),
          "stock": product.get_stock(),
          "history": product.get_history(),
      }

      if isinstance(product, PhysicalProduct):
        record["type"] = "physical"
        record["weight"] = product.get_weight()
      elif isinstance(product, DigitalProduct):
        record["type"] = "digital"
        record["download_size"] = product.get_download_size()

      data.append(record)

    with open(self.file_name, "w") as file:
      json.dump(data, file, indent=4)

  def load_products(self, path: str, inventory, supplier) -> None:
    """Loads products from a CSV file using try/except/else/finally."""
    loaded = 0
    try:
      file = open(path, newline="")
    except FileNotFoundError:
      print(f"Products file not found: {path}")
    else:
      with file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row

        for row_index, row in enumerate(reader, start=2):
          if not row:
            continue
          try:
            product_type, product_id, name, price_str, stock_str = [
                col.strip() for col in row
            ]
            price = float(price_str)
            stock_quantity = int(stock_str)

            # Create product via your factory[cite: 8]
            if product_type == "physical":
              product = ProductFactory.create(
                  product_type,
                  product_id,
                  name,
                  price,
                  stock_quantity,
                  supplier,
                  weight=1.0,
              )
            elif product_type == "digital":
              product = ProductFactory.create(
                  product_type,
                  product_id,
                  name,
                  price,
                  stock_quantity,
                  supplier,
                  download_size=10.0,
              )
            else:
              raise ValueError(f"Unknown product type: {product_type}")

            inventory.add_product(product)
            loaded += 1
          except ValueError as e:
            print(f"Skipping row {row_index} due to error: {e}")

        print(f"{loaded} products loaded.")
    finally:
      print("Load attempt finished.")

