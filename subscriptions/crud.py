from sqlalchemy.orm import Session
from . import models, schemas


def list_subscriptions(db: Session, skip: int = 0, limit: int = 100, app_name: str = None, event: str = None):
    query = db.query(models.Subscription)
    if app_name:
        query = query.filter(models.Subscription.app_name == app_name)
    if event:
        query = query.filter((models.Subscription.event == event) | (models.Subscription.event == '*'))
    return query.offset(skip).limit(limit).all()


def get_subscription(db: Session, pk: int) -> models.Subscription:
    return db.query(models.Subscription).filter(models.Subscription.id == pk).first()


def delete_subscription(db: Session, item: models.Subscription):
    db.delete(item)
    db.commit()
    return item


def create_subscription(db: Session, new: schemas.Subscription):
    new_item = new.dict()
    del new_item['id']
    db_item = models.Subscription(**new_item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item




