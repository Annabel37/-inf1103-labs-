from orderline import OrderLine
from product import Product
from DiscountStrategy import DiscountStrategy
from NoDiscount import NoDiscount
# Make sure to import your strategies if they are in another file:
# from discount_strategy import DiscountStrategy, NoDiscount


class Order:

  def __init__(
      self,
      order_id: str,
      order_lines: list[OrderLine] = None,
      strategy: DiscountStrategy = None,
  ):
    self.order_id: str = order_id
    # Aggregation for orderline
    self.order_lines: list[OrderLine] = (
        order_lines if order_lines is not None else []
    )

    # If no strategy is provided when created, default to NoDiscount()
    self.strategy: DiscountStrategy = (
        strategy if strategy is not None else NoDiscount()
    )

  def add_order_line(self, product: Product, quantity: int) -> None:
    order_line = OrderLine(product, quantity)
    self.order_lines.append(order_line)

  def remove_order_line(self, product_id: str) -> None:
    self.order_lines = [
        line
        for line in self.order_lines
        if line.product.get_product_id() != product_id
    ]

  def set_discount(self, strategy: DiscountStrategy) -> None:
    """Allows changing the discount strategy later."""
    self.strategy = strategy

  def calculate_subtotal(self) -> float:
    """Calculates the raw sum of order lines without any discounts applied."""
    total = 0.0
    for order_line in self.order_lines:
      total += order_line.calculate_subtotal()
    return total

  def calculate_total(self) -> float:
    """Gets the raw subtotal and applies the current discount strategy."""
    raw_total = self.calculate_subtotal()
    return self.strategy.apply(raw_total)

#   def calculate_total(self) -> float: 
#     total = sum(line.calculate_subtotal() for line in self.order_lines) 
#     return self.discount.apply(total)   

    
    
