# Test script for INF1103 Lab 8 Requirements
from supplier import Supplier
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from inventory import Inventory
from order import Order
from orderline import OrderLine
from product import Product

def test_lsp_polymorphism(product: Product) -> None:
    """Helper function to test LSP and Polymorphism through the Product abstraction."""
    print(f"Testing Product: {product.get_name()}")
    # Both physical and digital products must support these methods correctly
    product.display_information()
    print(f"Fulfilment Info: {product.get_fulfilment_info()}")
    print("-" * 40)

def run_tests():
    print("=" * 50)
    print("STARTING LAB 8 AUTOMATED TESTS")
    print("=" * 50)

    # 1. Test Association: Supplier and Product
    print("\n[1] Testing Association (Supplier & Product)")
    supplier = Supplier("S999", "Global Tech Inc.", "support@globaltech.com")
    
    phys_prod = PhysicalProduct("P901", "Ergonomic Mouse", 45.00, 25, 0.3, supplier)
    digi_prod = DigitalProduct("D901", "Python E-Book", 19.99, 500, 15.5, supplier)
    
    # Verify supplier reference is correctly associated
    assert phys_prod.supplier.name == "Global Tech Inc."
    assert digi_prod.supplier.supplier_id == "S999"
    print("✓ Association test passed: Products successfully reference a Supplier object.")

    # 2. Test Aggregation: Inventory and Product
    print("\n[2] Testing Aggregation (Inventory & Product)")
    inventory = Inventory()
    
    # Adding independent products to inventory
    assert inventory.add_product(phys_prod) == True
    assert inventory.add_product(digi_prod) == True
    
    # Ensure duplicate product ID returns False
    assert inventory.add_product(PhysicalProduct("P901", "Duplicate", 10.0, 1, 1.0, supplier)) == False
    
    # Test removal: Removing from inventory must not destroy the product object itself
    inventory.remove_product("P901")
    assert inventory.search_product("P901") is None
    # Product still exists in memory and is fully operational
    assert phys_prod.get_name() == "Ergonomic Mouse"
    print("✓ Aggregation test passed: Inventory manages products without controlling their lifecycle.")

    # 3. Test Composition: Order and OrderLine
    print("\n[3] Testing Composition (Order & OrderLine)")
    order = Order("ORD-888")
    
    # Order creates and manages its own OrderLines internally via add_order_line
    order.add_order_line(phys_prod, 2)  # $45.00 * 2 = $90.00
    order.add_order_line(digi_prod, 3)  # $19.99 * 3 = $59.97
    
    assert len(order.order_lines) == 2
    expected_total = round((45.00 * 2) + (19.99 * 3), 2)
    assert order.calculate_total() == expected_total
    print(f"✓ Composition test passed: Order calculated correct total: ${order.calculate_total():.2f}")

    # 4. Test LSP & Polymorphism
    print("\n[4] Testing Liskov Substitution Principle & Polymorphism")
    # Passing subclasses wherever parent class Product is expected
    test_lsp_polymorphism(phys_prod)
    test_lsp_polymorphism(digi_prod)
    print("✓ LSP & Polymorphism test passed: Subclasses seamlessly executed overridden methods.")

    print("\n" + "=" * 50)
    print("ALL LAB 8 TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 50)

if __name__ == "__main__":
    run_tests()