import pytest
from faker import Faker
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from starlette.testclient import TestClient
from coworld.api import create_app
from coworld.controllers.dishes import DishController
from coworld.controllers.menus import MenuController
from coworld.controllers.reservations import ReservationController


@pytest.fixture(name="engine")
def fixture_engine():
    sqlite_url = "sqlite://"
    engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def fixture_session(engine) -> Session:
    with Session(engine) as session:
        yield session


@pytest.fixture(name="dish_controller")
def dish_controller(session) -> DishController:
    return DishController(session)


@pytest.fixture(name="menu_controller")
def menu_controller(session) -> MenuController:
    return MenuController(session)


@pytest.fixture(name="reservation_controller")
def reservation_controller(session) -> ReservationController:
    return ReservationController(session)


@pytest.fixture(name="faker")
def get_faker() -> Faker:
    return Faker("fr_FR")


@pytest.fixture(name="app")
def get_test_app() -> FastAPI:
    return create_app()


@pytest.fixture(name="client")
def get_test_client(app: FastAPI) -> TestClient:
    return TestClient(app)
