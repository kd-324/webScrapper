def get_scrapper_service():
    from app.services.scrapper_service import ScrapperService
    return ScrapperService()

def get_scrapper_dao():
    from app.dao.impl.scrapper_dao_local import ScrapperDaoLocal
    return ScrapperDaoLocal()

def get_notification_service():
    from app.services.impl.notification_service_console import NotificationServiceConsole
    return NotificationServiceConsole()