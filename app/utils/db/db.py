from abc import ABC
from typing import List

from app.models.product import Product


class StorageStrategy(ABC):
    def save(self, products: List[Product]):
        pass
    def load(self) -> List[Product]:
        pass