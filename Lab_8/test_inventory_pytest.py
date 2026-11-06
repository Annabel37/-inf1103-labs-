import pytest
from supplier import Supplier
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from inventory import Inventory
from order import Order
from orderline import OrderLine
from product import Product

@pytest.fixture
def sample_supplier():
    """Fixture to provide a standard Supplier instance."""
    return Supplier("S001", "TechDistributor", "sales@techdist.com")

@pytest.fixture
def physical_item(sample_supplier):
    """Fixture to provide a PhysicalProduct instance."""
    return PhysicalProduct("P001", "Laptop", 1200.00, 10, 2.5, sample_supplier)

@pytest.fixture
def digital_item(sample_supplier):
    """Fixture to provide a DigitalProduct instance."""
    return DigitalProduct("D001", "Cloud Storage 1TB", 99.99, 50, 500.0, sample_supplier)

@pytest.fixture
def populated_inventory(physical_item, digital_item):
    """Fixture to provide an Inventory pre-populated with products."""
    inv = Inventory()
    inv.add_product(physical_item)
    inv.add_product(digital_item)
    return inv


# --- 1. Association Tests (Supplier & Product) ---
def test_supplier_association(physical_item, sample_supplier):
    """Verify that Product is properly associated with a Supplier."""
    assert physical_item.supplier == sample_supplier
    assert physical_item.supplier.name == "TechDistributor"
    assert physical_item.supplier.contact_email == "sales@techdist.com"


# --- 2. Aggregation Tests (Inventory & Product) ---
def test_inventory_add_and_search(populated_inventory, physical_item):
    """Verify adding products and searching within the inventory."""
    found = populated_inventory.search_product("P001")
    assert found == physical_item
    assert found.get_name() == "Laptop"

def test_inventory_duplicate_addition(populated_inventory, sample_supplier):
    """Verify that duplicate product IDs cannot be added."""
    duplicate = PhysicalProduct("P001", "Another Laptop", 900.00, 5, 2.0, sample_supplier)
    result = populated_inventory.add_product(duplicate)
    assert result is False

def test_inventory_remove_product(populated_inventory, physical_item):
    """Verify aggregation property: removing a product detaches it without destroying it."""
    populated_inventory.remove_product("P001")
    assert populated_inventory.search_product("P001") is None
    # The product object itself still exists and functions independently
    assert physical_item.get_stock() == 10


# --- 3. Composition Tests (Order & OrderLine) ---
def test_order_composition_and_total(physical_item, digital_item):
    """Verify composition relationship: Order creates OrderLines and computes totals."""
    order = Order("ORD-100")
    order.add_order_line(physical_item, 2)  # 1200.00 * 2 = 2400.00
    order.add_order_line(digital_item, 1)   # 99.99 * 1 = 99.99

    assert len(order.order_lines) == 2
    assert isinstance(order.order_lines[0], OrderLine)
    
    expected_total = round((1200.00 * 2) + (99.99 * 1), 2)
    assert order.calculate_total() == expected_total


# --- 4. Liskov Substitution Principle & Polymorphism Tests ---
def test_polymorphic_fulfilment(physical_item, digital_item):
    """Verify subclasses implement the abstract Product methods polymorphically."""
    items = [physical_item, digital_item]
    
    fulfilments = [item.get_fulfilment_info() for item in items]
    assert "physical shipping" in fulfilments[0].lower()
    assert "digitally" in fulfilments[1].lower()

def test_shipping_cost_calculation(physical_item):
    """Verify physical product specific method works correctly."""
    # Weight is 2.5kg. Cost formula: round(2 + weight * 1.50, 2) -> 2 + 3.75 = 5.75
    assert physical_item.calculate_shipping_cost() == 5.75