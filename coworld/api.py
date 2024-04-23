from fastapi import FastAPI
from coworld.routes.dishes import router as dishes_router


def create_app():
    app = FastAPI()
    app.include_router(dishes_router)
    return app
