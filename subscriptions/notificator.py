import httpx
from sqlalchemy.orm import Session
from subscriptions.schemas import Notification
from subscriptions.crud import list_subscriptions


class Notificator:
    def __init__(self, notification: Notification, db: Session):
        self.__notification = notification
        self.__db = db

    async def notify_to_subscribers(self) -> (int, list[dict]):
        errors = []
        subscribers = list_subscriptions(self.__db,
                                         app_name=self.__notification.app_name,
                                         event=self.__notification.event)
        for x in subscribers:
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(x.callback_url, json=self.__notification.dict(), timeout=5)
            except Exception as e:
                errors.append({
                    'exception': repr(e),
                    'callback_url': x.callback_url
                })

        return len(subscribers), errors



