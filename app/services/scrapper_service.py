import time
import requests
from typing import List, Optional

from bs4 import BeautifulSoup

from app.models.product import Product
from app.services.notification.notify_strategy import NotificationStrategy
from app.utils.cache import Cache
from app.utils.db.db import StorageStrategy
from app.utils.image_utils import download_image

class ScrapperService:
    def __init__(self, base_url, page_limit: int, proxy: str, storage_strategy: StorageStrategy, notification_strategy: NotificationStrategy):
        self.base_url = base_url
        self.page_limit = page_limit
        self.proxies = {"http": proxy, "https": proxy} if proxy else None
        self.cache = Cache()
        self.storage = storage_strategy
        self.notification_strategy = notification_strategy

    def fetch_page(self, page_number: int, retries: int = 3, delay: int = 2) -> Optional[BeautifulSoup]:
        if page_number == 1:
            url = f"{self.base_url}"  # First page uses the base URL
        else:
            url = f"{self.base_url}page/{page_number}/"  # Subsequent pages use the page-specific URL

        print(f"Fetching URL: {url}")
        attempt = 0
        while attempt < retries:
            try:
                print(f"Fetching page {page_number} (Attempt {attempt + 1}/{retries})...")
                response = requests.get(url, proxies=self.proxies, timeout=10)
                response.raise_for_status()
                return BeautifulSoup(response.text, "html.parser")
            except requests.RequestException as e:
                print(f"Error fetching page {page_number}: {e}")
                attempt += 1
                if attempt < retries:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
        print(f"Failed to fetch page {page_number} after {retries} retries.")
        return None
    

    def scrape(self) -> List[Product]:
        """Scrape product data from the website."""
        all_products = []
        page_number = 1
        db_products = []
        while not self.page_limit or page_number <= self.page_limit:
            page_content = self.fetch_page(page_number)
            if not page_content:
                break

            product_elements = page_content.select("ul.products li")
            if not product_elements:
                print(f"No products found on page {page_number}. Stopping scrape.")
                break

            for index, element in enumerate(product_elements):
                title_element = element.select_one(".woo-loop-product__title a")
                if title_element:
                    product_title = title_element.text.strip()
                else:
                    continue
                price_element = element.find('ins')
                if not price_element:
                    price_element = element.find('span', class_='woocommerce-Price-amount')
                
                if price_element:
                    price_text = price_element.get_text(strip=True).replace('₹', '').replace(',', '')
                    product_price = float(price_text)
                
                image_element = element.find("img")
                if image_element:
                    image_url = (
                        image_element.get('data-lazy-src') or 
                        image_element.get('src')
                    )
                else:
                    image_url = None
                cached_product_key = product_title+f"-{page_number}-{index}"
                cached_product_price = self.cache.get(cached_product_key)
                image_path = download_image(image_url, product_title)

    
                product = Product(
                    product_title=product_title,
                    product_price=product_price,
                    path_to_image=image_path,
                )
                all_products.append(product)

                self.cache.set(cached_product_key, product_price)
                if not cached_product_price or cached_product_price != product_price:
                    print("product db", product)
                    db_products.append(product)                

            page_number += 1
        if(len(db_products) > 0):
            self.storage.save(db_products)

        self.notification_strategy.sendNotifications(scraped_products=len(all_products), updated_products= len(db_products))
        return all_products 