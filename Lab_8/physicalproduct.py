
from product import Product 
from canbeshipped import CanBeShipped
from supplier import Supplier

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float, supplier: Supplier, history: list[int] = None):
        super().__init__(product_id, name, price, stock, supplier, history)
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def get_fulfilment_info(self) -> str:
        return "The Product requires physical shipping"

    def calculate_shipping_cost(self) -> float:
        return round(2 + self.__weight * 1.50, 2)

    def display_summary(self) -> None:
        super().display_summary()
        print("  -> Requires physical shipping")
