from product import Product
from supplier import Supplier

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float, supplier: Supplier, history: list[int] = None):
        super().__init__(product_id, name, price, stock, supplier, history)
        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download size: {self.__download_size} MB")

    def display_summary(self) -> None:
        super().display_summary()
        print("  -> Delivered digitally")

    def get_fulfilment_info(self) -> str:
        return "The product is delivered digitally"
        
