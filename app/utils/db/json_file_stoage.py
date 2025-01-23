import json
import os
from typing import List
from app.models.product import Product
from app.utils.db.db import StorageStrategy

FILE_URL = "products.json"
class JsonFileStorage(StorageStrategy):
    def save(self, products: List[Product]) -> None:
        new_data = [product.dict() for product in products]
        
        if os.path.exists(FILE_URL):
            with open(FILE_URL, "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = []
        
        existing_data.extend(new_data)

        with open(FILE_URL, "w") as file:
            json.dump(existing_data, file, indent=4)

        print(f"Data saved to {FILE_URL}")

    def load(self) -> List[Product]:
        try:
            with open(FILE_URL, "r") as file:
                data = json.load(file)
            return [Product(**item) for item in data]
        except FileNotFoundError:
            print(f"{FILE_URL} not found. Returning empty list.")
            return []
        