import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from coworld.controllers.menus import MenuController
from coworld.dependencies import get_menu_controller
from coworld.models.errors import MenuNotFoundError
from coworld.models.models import Menu


@pytest.mark.asyncio
async def test_get_menu_by_id(
    menu_controller: MenuController, app: FastAPI, client: TestClient
):
    _id = uuid.uuid4()

    def _mock_get_menu_by_id():
        menu_controller.get_menu_by_id = AsyncMock(
            return_value=Menu(
                id=_id,
                created_at=datetime(2020, 1, 1),
                title="Amazing Cow",
                description="The Amazing Cow menu, juicy and tasty.",
                price=6.99,
                discount=0.0,
            ),
        )
        return menu_controller

    app.dependency_overrides[get_menu_controller] = _mock_get_menu_by_id

    get_menu_by_id_response = client.get(f"/menus/{_id}")
    assert get_menu_by_id_response.status_code == 200
    assert get_menu_by_id_response.json() == {
        "id": str(_id),
        "created_at": "2020-01-01T00:00:00",
        "title": "Amazing Cow",
        "description": "The Amazing Cow menu, juicy and tasty.",
        "price": 6.99,
        "discount": 0.0,
        "discounted_price": 6.99,
    }


@pytest.mark.asyncio
async def test_get_menu_by_id_raise_no_result_found_error(
    menu_controller: MenuController, app: FastAPI, client: TestClient
):
    _id = uuid.uuid4()

    def _mock_get_menu_by_id():
        menu_controller.get_menu_by_id = AsyncMock(
            side_effect=MenuNotFoundError(menu_id=_id)
        )
        return menu_controller

    app.dependency_overrides[get_menu_controller] = _mock_get_menu_by_id

    get_menu_by_id_response = client.get(f"/menus/{_id}")
    assert get_menu_by_id_response.status_code == 404
    assert get_menu_by_id_response.json() == {
        "message": f"Menu with ID {_id} not found",
        "name": "MenuNotFoundError",
        "status_code": 404,
    }


@pytest.mark.asyncio
async def test_get_menus(
    menu_controller: MenuController, app: FastAPI, client: TestClient
):
    mock_menus = [
        Menu(
            id=uuid.uuid4(),
            created_at=datetime(2020, 1, 1),
            title="Amazing Cow",
            description="The Amazing Cow menu, juicy and tasty.",
            price=6.99,
            discount=0.0,
        ),
        Menu(
            id=uuid.uuid4(),
            created_at=datetime(2023, 3, 3),
            title="Amazing Coworld",
            description="The Amazing Coworld menu, juicy and tasty.",
            price=8.99,
            discount=20.0,
        ),
    ]

    def _mock_get_menus():
        menu_controller.get_menus = AsyncMock(return_value=mock_menus)
        return menu_controller

    app.dependency_overrides[get_menu_controller] = _mock_get_menus

    get_menus_response = client.get("/menus")
    assert get_menus_response.status_code == 200
    assert get_menus_response.json() == [
        {
            "id": str(menu.id),
            "created_at": menu.created_at.isoformat(),
            "title": menu.title,
            "description": menu.description,
            "price": menu.price,
            "discount": menu.discount,
            "discounted_price": menu.discounted_price,
            "dishes": [],
        }
        for menu in mock_menus
    ]
