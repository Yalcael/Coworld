from fastapi import Depends
from sqlmodel import Session

from coworld.controllers.dishs import DishController
from coworld.database import engine


def get_session() -> Session:
    with Session(engine) as session:
        yield session


def get_dish_controller(session=Depends(get_session)):
    return DishController(session)
