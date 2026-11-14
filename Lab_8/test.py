# Test script for INF1103 Lab 9 Requirements
from digitalproduct import DigitalProduct
from DiscountStrategy import DiscountStrategy
from BulkDiscount import BulkDiscount
from PercentageDiscount import PercentageDiscount
from inventory import Inventory
from order import Order
from orderline import OrderLine
from physicalproduct import PhysicalProduct
from product import Product
from ProductFactory import ProductFactory
from supplier import Supplier


# Helper function (does NOT start with 'test_' so pytest ignores it as a fixture)
def helper_lsp_polymorphism(product: Product) -> None:
  print(f"Testing Product: {product.get_name()}")
  product.display_information()
  print(f"Fulfilment Info: {product.get_fulfilment_info()}")
  print("-" * 40)


# Individual test functions for pytest (must start with 'test_')
def test_factory_and_association():
  print("\n[1 & 2] Testing Factory Pattern & Association")
  supplier = Supplier("S999", "Global Tech Inc.", "support@globaltech.com")

  phys_prod = ProductFactory.create(
      "physical", "P901", "Ergonomic Mouse", 45.00, 25, supplier, weight=0.3
  )
  digi_prod = ProductFactory.create(
      "digital",
      "D901",
      "Python E-Book",
      19.99,
      500,
      supplier,
      download_size=15.5,
  )

  assert phys_prod.supplier.name == "Global Tech Inc."
  assert digi_prod.supplier.supplier_id == "S999"
  print("✓ Factory & Association test passed.")

  # Test Factory ValueError for unknown type
  try:
    ProductFactory.create(
        "service", "S901", "Installation", 30.00, 5, supplier
    )
    assert False, "Should have raised ValueError"
  except ValueError as e:
    print(f"✓ Factory Exception test passed: {e}")


def test_validation_rules():
  print("\n[3] Testing Validation Rules")
  supplier = Supplier("S999", "Global Tech Inc.", "support@globaltech.com")
  phys_prod = ProductFactory.create(
      "physical", "P901", "Ergonomic Mouse", 45.00, 25, supplier, weight=0.3
  )

  try:
    ProductFactory.create(
        "physical", "P999", "Bad Price", -10.00, 10, supplier, weight=1.0
    )
    assert False
  except ValueError:
    print("✓ Validation passed: Negative price correctly rejected.")

  try:
    OrderLine(phys_prod, 0)
    assert False
  except ValueError:
    print("✓ Validation passed: Zero quantity order line correctly rejected.")


def test_strategy_pattern():
  print("\n[4] Testing Strategy Pattern (Order Discounts)")
  supplier = Supplier("S999", "Global Tech Inc.", "support@globaltech.com")
  order = Order("ORD-999")
  expensive_prod = ProductFactory.create(
      "physical", "P999", "Super Laptop", 250.00, 5, supplier, weight=2.0
  )
  order.add_order_line(expensive_prod, 1)

  # Test default NoDiscount
  assert order.calculate_total() == 250.00
  print("✓ Default Strategy test passed: Uses NoDiscount by default.")

  # Test BulkDiscount (200, 20) -> 250 - 20 = 230
  order.set_discount(BulkDiscount(200, 20))
  assert order.calculate_total() == 230.00
  print("✓ BulkDiscount test passed.")

  # Test PercentageDiscount(10) -> 250 * 0.90 = 225
  order.set_discount(PercentageDiscount(10))
  assert order.calculate_total() == 225.00
  print("✓ PercentageDiscount test passed.")


def test_aggregation_and_lsp():
  print("\n[5 & 6] Testing Aggregation & Polymorphism")
  supplier = Supplier("S999", "Global Tech Inc.", "support@globaltech.com")
  phys_prod = ProductFactory.create(
      "physical", "P901", "Ergonomic Mouse", 45.00, 25, supplier, weight=0.3
  )
  digi_prod = ProductFactory.create(
      "digital",
      "D901",
      "Python E-Book",
      19.99,
      500,
      supplier,
      download_size=15.5,
  )

  inventory = Inventory()
  assert inventory.add_product(phys_prod) == True
  assert inventory.add_product(digi_prod) == True
  inventory.remove_product("P901")
  assert inventory.search_product("P901") is None
  print("✓ Aggregation test passed.")

  helper_lsp_polymorphism(phys_prod)
  helper_lsp_polymorphism(digi_prod)
  print("✓ LSP & Polymorphism test passed.")


if __name__ == "__main__":
  print("=" * 50)
  print("STARTING LAB 9 AUTOMATED TESTS")
  print("=" * 50)
  test_factory_and_association()
  test_validation_rules()
  test_strategy_pattern()
  test_aggregation_and_lsp()
  print("\n" + "=" * 50)
  print("ALL LAB 9 TESTS COMPLETED SUCCESSFULLY!")
  print("=" * 50)
