from fastapi import FastAPI
from domain import models
from domain.database import engine
from views.subscriptions_view import router as subscriptions_router

models.Base.metadata.create_all(bind=engine)

# TODO move to a config file
PREFIX = "/notification-service"

app = FastAPI(
    docs_url=f'{PREFIX}/docs'
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(subscriptions_router, prefix=PREFIX)
