import uuid
from datetime import datetime
from unittest.mock import AsyncMock
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from coworld.controllers.dishes import DishController
from coworld.dependencies import get_dish_controller
from coworld.models.dishes import Category
from coworld.models.errors import DishNotFoundError
from coworld.models.models import Dish


@pytest.mark.asyncio
async def test_get_dish_by_id(
    dish_controller: DishController, app: FastAPI, client: TestClient
):
    _id = uuid.uuid4()

    def _mock_get_dish_by_id():
        dish_controller.get_dish_by_id = AsyncMock(
            return_value=Dish(
                id=_id,
                created_at=datetime(2020, 1, 1),
                category=Category("PLATS"),
                title="Amazing Cow",
                description="The Amazing Cow burger, juicy and tasty.",
                ingredients="Meat, Salad, Tomato, Cheese",
                price=6.99,
                halal=False,
            ),
        )
        return dish_controller

    app.dependency_overrides[get_dish_controller] = _mock_get_dish_by_id

    get_dish_by_id_response = client.get(f"/dishes/{_id}")
    assert get_dish_by_id_response.status_code == 200
    assert get_dish_by_id_response.json() == {
        "id": str(_id),
        "created_at": "2020-01-01T00:00:00",
        "category": "PLATS",
        "title": "Amazing Cow",
        "description": "The Amazing Cow burger, juicy and tasty.",
        "ingredients": "Meat, Salad, Tomato, Cheese",
        "price": 6.99,
        "halal": False,
    }


@pytest.mark.asyncio
async def test_get_dish_by_id_raise_no_result_found_error(
    dish_controller: DishController, app: FastAPI, client: TestClient
):
    _id = uuid.uuid4()

    def _mock_get_dish_by_id():
        dish_controller.get_dish_by_id = AsyncMock(
            side_effect=DishNotFoundError(dish_id=_id)
        )
        return dish_controller

    app.dependency_overrides[get_dish_controller] = _mock_get_dish_by_id

    get_dish_by_id_response = client.get(f"/dishes/{_id}")
    assert get_dish_by_id_response.status_code == 404
    assert get_dish_by_id_response.json() == {
        "message": f"Dish with ID {_id} not found",
        "name": "DishNotFoundError",
        "status_code": 404,
    }
