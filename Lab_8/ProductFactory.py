from product import Product
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from supplier import Supplier
class ProductFactory:

  @staticmethod
  def create(
      product_type: str, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier, **kwargs,) -> Product:
    if product_type == "physical":
      weight = kwargs.get("weight", 1.0)
      return PhysicalProduct(
          product_id, name, price, stock_quantity, weight, supplier
      )
    elif product_type == "digital":
      download_size = kwargs.get("download_size", 10.0)
      return DigitalProduct(
          product_id, name, price, stock_quantity, download_size, supplier
      )
    else:
      raise ValueError(f"Unknown product type: {product_type}")