from app.dao.scrapper_dao import ScrapperDao
from typing import List, Dict
from app.models.product import Product

class ScrapperDaoDB(ScrapperDao):
    def get_product_details(self) -> Dict:
        pass

    def update_product_details(self, product_list: List[Product]) -> None:
        pass