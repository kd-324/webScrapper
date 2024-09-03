from app.dao.scrapper_dao import ScrapperDao
from typing import List, Dict
import os
import json

from app.models.product import Product


class ScrapperDaoLocal(ScrapperDao):
    def __init__(self):
        self.product_details = {}

    def get_product_details(self) -> Dict:
        if not self.product_details:
            self.product_details = self.fetch_data_from_file()

        return self.product_details

    def update_product_details(self, product_list: List[Product]) -> None:
        product_details = self.fetch_data_from_file()
        for product in product_list:
            product_details[product.product_title] = {'product_price': product.product_price, 'path_to_image': product.path_to_image}

        with open('app/assets/product_details', 'w') as file:
            json.dump(product_details, file)

        self.product_details = product_details

    def fetch_data_from_file(self):
        product_details = {}

        if os.path.exists('app/assets/product_details'):
            with open('app/assets/product_details', 'r') as file:
                product_details = json.load(file)

        return product_details