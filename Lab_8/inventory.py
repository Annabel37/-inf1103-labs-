# Inventory class (INF1103 Lab 6)
# Responsibility: manage a collection of Product objects.

from product import Product

class Inventory:
    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> None:
        """Remove the matching Product reference from the inventory."""
        self.__products = [p for p in self.__products if p.get_product_id() != product_id]

    def search_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def find_product(self, product_id: str) -> Product | None:
        return self.search_product(product_id)

    def display_all(self) -> None:
        line = "-" * 48
        print("Current Inventory")
        print(line)
        if len(self.__products) == 0:
            print("The inventory is empty.")
        for product in self.__products:
            product.display_summary()
        print(line)

    def get_products(self) -> list[Product]:
        return list(self.__products)