from fastapi import FastAPI, Depends, HTTPException
from controllers.notificator import Notificator
from domain.schemas import Notification
from sqlalchemy.orm import Session
from domain import crud, models, schemas
from domain.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/subscriptions/", response_model=list[schemas.Subscription])
def subscriptions_list(skip: int = 0, limit: int = 100, app_name: str = None, event: str = None, db: Session = Depends(get_db)):
    items = crud.list_subscriptions(db, skip=skip, limit=limit, app_name=app_name, event=event)
    return items


@app.post("/subscriptions/", response_model=schemas.Subscription)
def create_subscription(subscription: schemas.Subscription, db: Session = Depends(get_db)):
    item = crud.create_subscription(db, subscription)
    return item


@app.delete("/subscriptions/{pk}/", response_model=schemas.Subscription)
def delete_subscription(pk: int, db: Session = Depends(get_db)):
    item = crud.get_subscription(db, pk)
    if not item:
        raise HTTPException(detail='not found subscription', status_code=404)
    item = crud.delete_subscription(db, item)
    return item


@app.post("/notify/")
async def receive_notification(n: Notification, db: Session = Depends(get_db)):
    print("notify")
    notificator = Notificator(n, db)
    subscribers, errors = await notificator.notify_to_subscribers()
    return {
        'subscribers': subscribers,
        'notifications_sent': subscribers - len(errors),
        'errors': errors
    }
