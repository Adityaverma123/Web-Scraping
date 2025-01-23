from app.services.notification.notification_service import NotificationService


class SlackNotificationService(NotificationService):
    def notify(self,  scraped_products: int, updated_products: int):
        print(f"Slack Notification:")
        print(f"Total Product Scrapped: {scraped_products}")
        print(f"Total Products updated in DB: {updated_products}")