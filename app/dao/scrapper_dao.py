from abc import ABC, abstractmethod
from typing import List, Dict

from app.models.product import Product


class ScrapperDao(ABC):
    @abstractmethod
    def get_product_details(self) -> Dict:
        pass

    @abstractmethod
    def update_product_details(self, product_list: List[Product]) -> None:
        pass