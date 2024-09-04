from app.services.notification_service import NotificationService


class NotificationServiceConsole(NotificationService):
    def notify_user(self, username: str, address: str = 'not applicable'):
        print('scape job has been completed @' + username)