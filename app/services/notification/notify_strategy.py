from typing import List
from app.models.notfication_channel import NotificationChannel
from app.services.notification.console_notification import ConsoleNotificationService
from app.services.notification.slack_notification import SlackNotificationService


class NotificationStrategy:
    def __init__(self, channels: List[NotificationChannel]):
        self.channels = channels

    def sendNotifications(self, scraped_products: int, updated_products: int):
        for channel in self.channels:
            if channel == NotificationChannel.CONSOLE:
                notification = ConsoleNotificationService()
            elif channel == NotificationChannel.SLACK:
                notification = SlackNotificationService()
            else:
                raise ValueError(f"Unsupported notification channel: {channel}")
            notification.notify(scraped_products= scraped_products, updated_products= updated_products)