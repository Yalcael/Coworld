import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from coworld.controllers.menus import MenuController
from coworld.dependencies import get_menu_controller
from coworld.models.errors import MenuNotFoundError, MenuAlreadyExistsError
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


@pytest.mark.asyncio
async def test_create_menu(
    menu_controller: MenuController, app: FastAPI, client: TestClient
):
    menu_data = {
        "title": "Amazing Cow",
        "description": "The Amazing Cow menu, juicy and tasty.",
        "price": 6.99,
        "discount": 0.0,
        "discounted_price": 6.99,  # This should not be part of input data
    }

    mock_menu = Menu(
        id=uuid.uuid4(),
        created_at=datetime(2020, 1, 1),
        title=menu_data["title"],
        description=menu_data["description"],
        price=menu_data["price"],
        discount=menu_data["discount"],
    )

    def _mock_create_menu():
        menu_controller.create_menu = AsyncMock(return_value=mock_menu)
        return menu_controller

    app.dependency_overrides[get_menu_controller] = _mock_create_menu

    create_menu_response = client.post("/menus", json=menu_data)
    assert create_menu_response.status_code == 201
    assert create_menu_response.json() == {
        "id": str(mock_menu.id),
        "created_at": mock_menu.created_at.isoformat(),
        "title": mock_menu.title,
        "description": mock_menu.description,
        "price": mock_menu.price,
        "discount": mock_menu.discount,
        "discounted_price": mock_menu.discounted_price,
    }


@pytest.mark.asyncio
async def test_create_menu_raise_menu_already_exists_error(
    menu_controller: MenuController, app: FastAPI, client: TestClient
):
    menu_data = {
        "title": "Amazing Cow",
        "description": "The Amazing Cow menu, juicy and tasty.",
        "price": 6.99,
        "discount": 0.0,
        # Remove `discounted_price` from the input data
    }

    def _mock_create_menu():
        menu_controller.create_menu = AsyncMock(
            side_effect=MenuAlreadyExistsError(title=menu_data["title"])
        )
        return menu_controller

    # Correctly set the dependency override
    app.dependency_overrides[get_menu_controller] = _mock_create_menu

    create_menu_response = client.post("/menus", json=menu_data)
    assert create_menu_response.status_code == 409
    assert create_menu_response.json() == {
        "name": "MenuAlreadyExistsError",
        "message": f"Menu with title: {menu_data['title']} already exists",
        "status_code": 409,
    }


@pytest.mark.asyncio
async def test_update_menu(
    menu_controller: MenuController, app: FastAPI, client: TestClient
):
    _id = uuid.uuid4()
    menu_update_data = {
        "title": "Amazing Cow",
        "description": "The Amazing Cow menu, juicy and tasty.",
        "price": 6.99,
        "discount": 0.0,
        "discounted_price": 6.99,
    }

    updated_menu = Menu(
        id=_id,
        created_at=datetime(2020, 1, 1),
        title=menu_update_data["title"],
        description=menu_update_data["description"],
        price=menu_update_data["price"],
        discount=menu_update_data["discount"],
    )

    def _mock_update_menu():
        menu_controller.update_menu = AsyncMock(return_value=updated_menu)
        return menu_controller

    app.dependency_overrides[get_menu_controller] = _mock_update_menu

    update_menu_response = client.patch(f"/menus/{_id}", json=menu_update_data)

    assert update_menu_response.status_code == 200
    assert update_menu_response.json() == {
        "id": str(_id),
        "created_at": updated_menu.created_at.isoformat(),
        "title": updated_menu.title,
        "description": updated_menu.description,
        "price": updated_menu.price,
        "discount": updated_menu.discount,
        "discounted_price": updated_menu.discounted_price,
    }


@pytest.mark.asyncio
async def test_update_menu_not_found_error(
    menu_controller: MenuController, client: TestClient, app: FastAPI
):
    _id = uuid.uuid4()

    menu_update_data = {
        "title": "Amazing Cow",
        "description": "The Amazing Cow menu, juicy and tasty.",
        "price": 6.99,
        "discount": 0.0,
        "discounted_price": 6.99,
    }

    def _mock_update_menu():
        menu_controller.update_menu = AsyncMock(
            side_effect=MenuNotFoundError(menu_id=_id)
        )
        return menu_controller

    app.dependency_overrides[get_menu_controller] = _mock_update_menu
    update_menu_response = client.patch(f"/menus/{_id}", json=menu_update_data)
    assert update_menu_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_menu(
    menu_controller: MenuController, app: FastAPI, client: TestClient
):
    _id = uuid.uuid4()

    def _mock_delete_menu():
        menu_controller.delete_menu = AsyncMock(return_value=None)
        return menu_controller

    app.dependency_overrides[get_menu_controller] = _mock_delete_menu
    delete_menu_response = client.delete(f"/menus/{_id}")
    assert delete_menu_response.status_code == 204


@pytest.mark.asyncio
async def test_delete_menu_not_found_error(
    app: FastAPI, client: TestClient, menu_controller: MenuController
):
    _id = uuid.uuid4()

    def _mock_delete_menu():
        menu_controller.delete_menu = AsyncMock(
            side_effect=MenuNotFoundError(menu_id=_id)
        )
        return menu_controller

    app.dependency_overrides[get_menu_controller] = _mock_delete_menu
    delete_menu_response = client.delete(f"/menus/{_id}")
    assert delete_menu_response.status_code == 404
