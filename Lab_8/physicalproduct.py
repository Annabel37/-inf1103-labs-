
from product import Product 
from canbeshipped import CanBeShipped



class PhysicalProduct(Product, CanBeShipped):
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

    def calculate_shipping_cost(self):
        # $2 shipping fee + $1.50 for each kg
        return round(2 + self.__weight * 1.50, 2)

    def display_summary(self):
        super().display_summary()
        return f"The Product required physical shipping"
       # print("  The product requires physical shipping")
