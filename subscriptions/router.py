from fastapi import Depends, HTTPException, APIRouter
from subscriptions.notificator import Notificator
from subscriptions.database import get_db
from subscriptions.schemas import Notification
from sqlalchemy.orm import Session
from subscriptions import crud, schemas

router = APIRouter(prefix="/subscriptions")


@router.get("/", response_model=list[schemas.Subscription])
def subscriptions_list(skip: int = 0, limit: int = 100, app_name: str = None, event: str = None, db: Session = Depends(get_db)):
    items = crud.list_subscriptions(db, skip=skip, limit=limit, app_name=app_name, event=event)
    return items


@router.post("/", response_model=schemas.Subscription)
def create_subscription(subscription: schemas.Subscription, db: Session = Depends(get_db)):
    item = crud.create_subscription(db, subscription)
    return item


@router.delete("/{pk}/", response_model=schemas.Subscription)
def delete_subscription(pk: int, db: Session = Depends(get_db)):
    item = crud.get_subscription(db, pk)
    if not item:
        raise HTTPException(detail='not found subscription', status_code=404)
    item = crud.delete_subscription(db, item)
    return item


@router.post("/notify/")
async def receive_notification(n: Notification, db: Session = Depends(get_db)):
    print("notify")
    notificator = Notificator(n, db)
    subscribers, errors = await notificator.notify_to_subscribers()
    return {
        'subscribers': subscribers,
        'notifications_sent': subscribers - len(errors),
        'errors': errors
    }
