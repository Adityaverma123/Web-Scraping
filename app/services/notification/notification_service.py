from abc import ABC, abstractmethod


class NotificationService(ABC):
    @abstractmethod
    def notify(self,  scraped_products: int, updated_products: int):
        pass