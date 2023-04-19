from fastapi import FastAPI
from domain import models
from domain.database import engine
from views.subscription_views import router as subscriptions_router

models.Base.metadata.create_all(bind=engine)

# TODO move to a config file
PREFIX = "/notification-service"

app = FastAPI(
    title="Notification service",
    description="App for notify to subscribers by app_name and event name",
    version="0.0.1",
    docs_url=f'{PREFIX}/docs',
    openapi_url=f'{PREFIX}/openapi.json'
)

app.include_router(subscriptions_router, prefix=PREFIX)
