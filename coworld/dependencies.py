from typing import Generator

from fastapi import Depends
from sqlmodel import Session

from coworld.controllers.dishes import DishController
from coworld.controllers.menus import MenuController
from coworld.controllers.reservations import ReservationController
from coworld.database import engine


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_dish_controller(session=Depends(get_session)):
    return DishController(session)


def get_menu_controller(session=Depends(get_session)):
    return MenuController(session)


def get_reservation_controller(session=Depends(get_session)):
    return ReservationController(session)
