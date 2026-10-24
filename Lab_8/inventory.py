# Inventory class (INF1103 Lab 6)
# Responsibility: manage a collection of Product objects.

class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Add a product. Return False if the ID already exists."""
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        """Return the product with this ID. Return None if not found."""
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self):
        """Show each product on one line."""
        line = "-" * 48
        print("Current Inventory")
        print(line)
        if len(self.__products) == 0:
            print("The inventory is empty.")
        for product in self.__products:
            product.display_summary()
        print(line)

    def get_products(self):
        """Return a copy of the product list (used when saving)."""
        return list(self.__products)