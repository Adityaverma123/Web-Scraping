from app.models.product import Product
# Why singleton?

## Because we don't want to creeate new Cache instance everytime Api is called
class Cache:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.dict = {}
        return cls.instance

    def get(self, key: str) -> float:
        return self.dict.get(key)
    
    def set(self, key: str, price: float):
        self.dict[key] = price
    
    def clear(self):
        self.dict.clear()