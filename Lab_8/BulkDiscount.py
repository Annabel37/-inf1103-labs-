from PercentageDiscount import PercentageDiscount
from NoDiscount import NoDiscount

from DiscountStrategy import DiscountStrategy
class BulkDiscount(DiscountStrategy):

  def __init__(self, threshold: float, amount: float):
    self.threshold = threshold
    self.amount = amount

  def apply(self, total: float) -> float:
    if total >= self.threshold:
      return total - self.amount
    return total


ten_percent_off = PercentageDiscount(10)
twenty_off_two_hundred = BulkDiscount(200, 20)
standard = NoDiscount()

# Applying them to an order total
print(ten_percent_off.apply(100))  # Output: 90.0
print(twenty_off_two_hundred.apply(250))  # Output: 230.0
print(standard.apply(50))  # Output: 50