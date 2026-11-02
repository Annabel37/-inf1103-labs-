from product import Product

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size, history=None):
        super().__init__(product_id, name, price, stock, history)
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"Download size: {self.__download_size} MB")

    def display_summary(self):
        super().display_summary()
        return f"The Product delivered digitally"
        # print("  The product deliver degitally")

    def get_fulfilment_info(self):
        return f"the product is delivered digitally"
        
