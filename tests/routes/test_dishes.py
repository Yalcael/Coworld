import uuid
from datetime import datetime
from unittest.mock import AsyncMock
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from coworld.controllers.dishes import DishController
from coworld.dependencies import get_dish_controller
from coworld.models.dishes import Category
from coworld.models.errors import DishNotFoundError, DishAlreadyExistsError
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


@pytest.mark.asyncio
async def test_get_dishes(
    dish_controller: DishController, app: FastAPI, client: TestClient
):
    mock_dishes = [
        Dish(
            id=uuid.uuid4(),
            created_at=datetime(2020, 1, 1),
            category=Category("PLATS"),
            title="Amazing Cow",
            description="The Amazing Cow burger, juicy and tasty.",
            ingredients="Meat, Salad, Tomato, Cheese",
            price=6.99,
            halal=False,
        ),
        Dish(
            id=uuid.uuid4(),
            created_at=datetime(2024, 2, 2),
            category=Category("DRINKS"),
            title="Amazing Milk",
            description="The Amazing Cow Milk, juicy and tasty.",
            ingredients="Milk",
            price=2.99,
            halal=True,
        ),
    ]

    def _mock_get_dishes():
        dish_controller.get_dishes = AsyncMock(return_value=mock_dishes)
        return dish_controller

    app.dependency_overrides[get_dish_controller] = _mock_get_dishes

    get_dishes_response = client.get("/dishes")
    assert get_dishes_response.status_code == 200
    assert get_dishes_response.json() == [
        {
            "id": str(dish.id),
            "created_at": dish.created_at.isoformat(),
            "category": dish.category.name,
            "title": dish.title,
            "description": dish.description,
            "ingredients": dish.ingredients,
            "price": dish.price,
            "halal": dish.halal,
            "menus": [],
        }
        for dish in mock_dishes
    ]


@pytest.mark.asyncio
async def test_create_dish(
    dish_controller: DishController, app: FastAPI, client: TestClient
):
    dish_data = {
        "category": "PLATS",
        "title": "Amazing Cow",
        "description": "The Amazing Cow burger, juicy and tasty.",
        "ingredients": "Meat, Salad, Tomato, Cheese",
        "price": 6.99,
        "halal": False,
    }

    mock_dish = Dish(
        id=uuid.uuid4(),
        created_at=datetime(2020, 1, 1),
        category=Category(dish_data["category"]),
        **{k: v for k, v in dish_data.items() if k != "category"},
    )

    def _mock_create_dish():
        dish_controller.create_dish = AsyncMock(return_value=mock_dish)
        return dish_controller

    app.dependency_overrides[get_dish_controller] = _mock_create_dish

    create_dish_response = client.post("/dishes", json=dish_data)
    assert create_dish_response.status_code == 201
    assert create_dish_response.json() == {
        "id": str(mock_dish.id),
        "created_at": mock_dish.created_at.isoformat(),
        "category": mock_dish.category.name,
        "title": mock_dish.title,
        "description": mock_dish.description,
        "ingredients": mock_dish.ingredients,
        "price": mock_dish.price,
        "halal": mock_dish.halal,
    }


@pytest.mark.asyncio
async def test_create_dish_raise_dish_already_exists_error(
    dish_controller: DishController, app: FastAPI, client: TestClient
):
    dish_data = {
        "category": "PLATS",
        "title": "Amazing Cow",
        "description": "The Amazing Cow burger, juicy and tasty.",
        "ingredients": "Meat, Salad, Tomato, Cheese",
        "price": 6.99,
        "halal": False,
    }

    def _mock_create_dish():
        dish_controller.create_dish = AsyncMock(
            side_effect=DishAlreadyExistsError(title=dish_data["title"])
        )
        return dish_controller

    app.dependency_overrides[get_dish_controller] = _mock_create_dish

    create_dish_response = client.post("/dishes", json=dish_data)
    assert create_dish_response.status_code == 409
    assert create_dish_response.json() == {
        "name": "DishAlreadyExistsError",
        "message": f"Dish with title: {dish_data['title']} already exists",
        "status_code": 409,
    }


@pytest.mark.asyncio
async def test_create_dish_bad_category(
    dish_controller: DishController, app: FastAPI, client: TestClient
):
    dish_data = {
        "category": "PLAT",  # It should be PLATS, PLAT is invalid category.
        "title": "Amazing Cow",
        "description": "The Amazing Cow burger, juicy and tasty.",
        "ingredients": "Meat, Salad, Tomato, Cheese",
        "price": 6.99,
        "halal": False,
    }

    def _mock_create_dish():
        dish_controller.create_dish = AsyncMock(side_effect=ValueError)
        return dish_controller

    app.dependency_overrides[get_dish_controller] = _mock_create_dish

    create_dish_response = client.post("/dishes", json=dish_data)
    assert create_dish_response.status_code == 422


@pytest.mark.asyncio
async def test_update_dish_(
    dish_controller: DishController, app: FastAPI, client: TestClient
):
    _id = uuid.uuid4()
    dish_update_data = {
        "title": "UpdatedAmazingCow",
        "category": "PLATS",
        "ingredients": "Meat, Salad, Tomato, Cheese, RealSauces",
        "description": "The Amazing Cow burger",
        "price": 8.99,
        "halal": False,
    }

    updated_dish = Dish(
        id=_id,
        created_at=datetime(2020, 1, 1),
        category=Category(dish_update_data["category"]),
        **{k: v for k, v in dish_update_data.items() if k != "category"},
    )

    def _mock_update_dish():
        dish_controller.update_dish = AsyncMock(return_value=updated_dish)
        return dish_controller

    app.dependency_overrides[get_dish_controller] = _mock_update_dish

    update_dish_response = client.patch(f"/dishes/{_id}", json=dish_update_data)
    assert update_dish_response.status_code == 200
    assert update_dish_response.json() == {
        "id": str(_id),
        "created_at": updated_dish.created_at.isoformat(),
        "category": updated_dish.category.name,
        "title": updated_dish.title,
        "description": updated_dish.description,
        "ingredients": updated_dish.ingredients,
        "price": updated_dish.price,
        "halal": updated_dish.halal,
    }


@pytest.mark.asyncio
async def test_update_dish_not_found_error(
    dish_controller: DishController, client: TestClient, app: FastAPI
):
    _id = uuid.uuid4()

    dish_update_data = {
        "title": "UpdatedAmazingCow",
        "category": "PLATS",
        "ingredients": "Meat, Salad, Tomato, Cheese, RealSauces",
        "description": "The Amazing Cow burger",
        "price": 8.99,
        "halal": False,
    }

    def _mock_update_dish():
        dish_controller.update_dish = AsyncMock(
            side_effect=DishNotFoundError(dish_id=_id)
        )
        return dish_controller

    app.dependency_overrides[get_dish_controller] = _mock_update_dish
    update_dish_response = client.patch(f"/dishes/{_id}", json=dish_update_data)
    assert update_dish_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_dish(
    dish_controller: DishController, app: FastAPI, client: TestClient
):
    _id = uuid.uuid4()

    def _mock_delete_dish():
        dish_controller.delete_dish = AsyncMock(return_value=None)
        return dish_controller

    app.dependency_overrides[get_dish_controller] = _mock_delete_dish
    delete_dish_response = client.delete(f"/dishes/{_id}")
    assert delete_dish_response.status_code == 204


@pytest.mark.asyncio
async def test_delete_dish_not_found_error(
    app: FastAPI, client: TestClient, dish_controller: DishController
):
    _id = uuid.uuid4()

    def _mock_delete_dish():
        dish_controller.delete_dish = AsyncMock(
            side_effect=DishNotFoundError(dish_id=_id)
        )
        return dish_controller

    app.dependency_overrides[get_dish_controller] = _mock_delete_dish
    delete_dish_response = client.delete(f"/dishes/{_id}")
    assert delete_dish_response.status_code == 404
