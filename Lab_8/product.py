# Product class (INF1103 Lab 6)
# Responsibility: represent and manage ONE product.
from abc import ABC, abstractmethod
from supplier import Supplier

class Product(ABC):
     
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, history: list[int] = None):
        if price < 0:
            raise ValueError("The price cannot be less than 0.")
        if stock < 0:
            raise ValueError("The stock cannot be less than 0.")

        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = round(price, 2)
        self.__stock: int = stock
        #creating a arregation with the supplier class
        self.supplier: Supplier = supplier
        
        if history is None:
            self.__history: list[int] = [stock]
        else:
            self.__history = list(history)

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def get_history(self) -> list[int]:
        return list(self.__history)

    def update_stock(self, quantity: int) -> int:
        if quantity < 0:
            raise ValueError("The stock cannot be less than 0.")
        change = quantity - self.__stock
        if change != 0:
            self.__stock = quantity
            self.__history.append(change)
        return change

    def display_information(self) -> None:
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(f"History: {self.__history}")
        if self.supplier:
            print("Supplier Details:")
            self.supplier.display_information()

    def display_summary(self) -> None:
        print(f"{self.get_product_id():<8} {self.get_name():<20} ${self.get_price():>8.2f} {self.get_stock():>5}")

    

   
        


   





    


# p = PhysicalProduct("P001", "mouse", 1, 2, 1)
# d = DigitalProduct("D001", "ebook", 5, 100, 25)

# p.display_information()
# print()
# d.display_information()
# print(p.get_fulfilment_info())
# print(d.get_fulfilment_info())

# light = PhysicalProduct("P001", "mouse", 20, 10, 0.2)
# medium = PhysicalProduct("P002", "keyboard", 50, 5, 1.5)
# heavy = PhysicalProduct("P003", "monitor", 200, 3, 6)

# for item in [light, medium, heavy]:
#     print(f"{item.get_name()} ({item.get_weight()} kg): ${item.calculate_shipping_cost():.2f}")

