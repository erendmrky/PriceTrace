from dataclasses import dataclass

@dataclass
class ProductResult:
    site: str
    title: str
    price: float