from abc import ABC


class NotificationService(ABC):
    def notify_user(self, username: str, address: str):
        pass