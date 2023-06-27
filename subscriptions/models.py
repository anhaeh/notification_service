import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, default='')
    app_name = Column(String)
    event = Column(String, default='*')
    callback_url = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
