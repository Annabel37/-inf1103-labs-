# Product class (INF1103 Lab 6)
# Responsibility: represent and manage ONE product.
from abc import ABC, abstractmethod

class Product(ABC):
    def __init__(self, product_id, name, price, stock, history=None):
        if price < 0:
            raise ValueError("The price cannot be less than 0.")
        if stock < 0:
            raise ValueError("The stock cannot be less than 0.")

        self.__product_id = product_id
        self.__name = name
        self.__price = round(price, 2)
        self.__stock = stock
        
        # The start stock is the first transaction in the history.
        if history is None:
            self.__history = [stock]
        else:
            self.__history = list(history)

    # ---------- Getters (read only access) ----------

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    @abstractmethod
    def get_fulfilment_info():
        pass

    

    def get_history(self):
        return list(self.__history)   # a copy, so outside code cannot change it

    # ---------- Methods ----------

    def update_stock(self, quantity):
        """Set a new stock quantity. Return the change (for example +10 or -5)."""
        if quantity < 0:
            raise ValueError("The stock cannot be less than 0.")

        change = quantity - self.__stock
        if change != 0:
            self.__stock = quantity
            self.__history.append(change)
        return change

    def display_information(self):
        """Show all details of this product."""
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(f"History: {self.__history}")

    def display_summary(self):
        """Show this product on one line."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
   
        



class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock, weight, history=None):
        super().__init__(product_id, name, price, stock, history)   # reuse Product constructor
        self.__weight = weight                                       # new attribute

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()          # show existing Product info
        print(f"Weight: {self.__weight} kg")   # add the new info

    def get_fulfilment_info(self):
        return f"The Product required physical shipping"


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size, history=None):
        super().__init__(product_id, name, price, stock, history)
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"Download size: {self.__download_size} MB")

    def get_fulfilment_info(self):
        return f"the product is delivered digitally"

    


# p = PhysicalProduct("P001", "mouse", 1, 2, 1)
# d = DigitalProduct("D001", "ebook", 5, 100, 25)

# p.display_information()
# print()
# d.display_information()
# print(p.get_fulfilment_info())
# print(d.get_fulfilment_info())