from product import Product
from orderline import OrderLine

class Order:
    def __init__(self, order_id: str, order_lines: list[OrderLine] = None):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = order_lines if order_lines is not None else []

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        total = 0.0
        for order_line in self.order_lines:
            total += order_line.calculate_subtotal()
        return total

    def remove_order_line(self, product_id: str) -> None:
        self.order_lines = [
            line for line in self.order_lines
            if line.product.get_product_id() != product_id
        ]
