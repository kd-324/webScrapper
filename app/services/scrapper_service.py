from typing import Dict, Any, List
from bs4 import BeautifulSoup
from app.models.product import Product
from httpx import AsyncClient
import re

from app.utils.dependencies import get_scrapper_dao, get_notification_service

JsonType = Dict[str, Any]

class ScrapperService:

    def __init__(self):
        self.scrapper_dao = get_scrapper_dao()
        self.notification_service = get_notification_service()
    async def scrape_website(self, page_count: int, proxy_string: str) -> None:
        products_to_update = await self.scrape_webpage(proxy_string)

        for i in range(2, page_count+1):
            products_at_next_page = await self.scrape_webpage(proxy_string + '/page/' + str(i))
            products_to_update.extend(products_at_next_page)

        self.scrapper_dao.update_product_details(products_to_update)
        self.notification_service.notify_user('user123')



    async def scrape_webpage(self, proxy_string: str) -> List[Product]:
        product_list_in_db = self.scrapper_dao.get_product_details()
        products_to_update = []

        async with AsyncClient() as client:
            response = await client.get(proxy_string)
            product_list = self.extract_product_details(response.content)

            for product in product_list:
                if (product.product_title in product_list_in_db
                        and product_list_in_db[product.product_title]['product_price'] == product.product_price):
                    continue
                else:
                    product.path_to_image = await self.save_image_to_local(product.product_title, product.path_to_image)
                    products_to_update.append(product)

        return products_to_update


    async def list_products(self) -> List[Dict]:
        product_list = []
        product_details = self.scrapper_dao.get_product_details()

        for product_name, properties in product_details.items():
            product_list.append(
                Product(product_title = product_name,
                        product_price=properties['product_price'],
                        path_to_image=properties['path_to_image'])
                .dict())

        return product_list


    def extract_product_details(self, webpage) -> List[Product]:
        product_list = []

        soup = BeautifulSoup(webpage, 'html.parser')
        elements = soup.find_all(class_='product-inner')

        for element in elements:
            title = element.find(class_='addtocart-buynow-btn').find('a').get('data-title')

            bdi_element = element.find('bdi')
            bdi_element.span.decompose()
            price = bdi_element.get_text()

            image_url = element.find(class_='mf-product-thumbnail').find('a').find('img').get('data-lazy-src')

            product_list.append(Product(product_title=title, product_price=price, path_to_image=image_url))

        return product_list

    async def save_image_to_local(self, product_title: str, image_url: str) -> str:
        file_name = re.sub('[^a-zA-Z0-9 ]', '', product_title).replace(' ', '_') + '.jpg'
        local_path = 'app/assets/product_images/' + file_name

        async with AsyncClient() as client:
            response = await client.get(image_url)
            with open(local_path, 'wb') as file:
                file.write(response.content)

        return local_path
