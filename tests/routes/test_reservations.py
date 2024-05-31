import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from pydantic_extra_types.phone_numbers import PhoneNumber
from starlette.testclient import TestClient

from coworld.controllers.reservations import ReservationController
from coworld.dependencies import get_reservation_controller
from coworld.models.errors import ReservationNotFoundError
from coworld.models.reservations import Reservation, ReservationCategory


@pytest.mark.asyncio
async def test_get_reservation_by_id(
    reservation_controller: ReservationController, app: FastAPI, client: TestClient
):
    _id = uuid.uuid4()

    def _mock_get_reservation_by_id():
        reservation_controller.get_reservation_by_id = AsyncMock(
            return_value=Reservation(
                id=_id,
                created_at=datetime(2020, 1, 1),
                reservation_category=ReservationCategory("SIMPLE"),
                name="aaaaaa",
                family_name="vvvvvv",
                amount_of_people=6,
                email_address="vvvvv@admin.com",
                reservation_time=datetime(2020, 3, 3, 20, 30, 0),
                phone_number=PhoneNumber("+33633445566"),
            ),
        )
        return reservation_controller

    app.dependency_overrides[get_reservation_controller] = _mock_get_reservation_by_id

    get_reservation_by_id_response = client.get(f"/reservations/{_id}")
    assert get_reservation_by_id_response.status_code == 200
    assert get_reservation_by_id_response.json() == {
        "id": str(_id),
        "created_at": "2020-01-01T00:00:00",
        "reservation_category": "SIMPLE",
        "name": "aaaaaa",
        "family_name": "vvvvvv",
        "amount_of_people": 6,
        "email_address": "vvvvv@admin.com",
        "reservation_time": "2020-03-03T20:30:00",
        "phone_number": "+33633445566",
    }


@pytest.mark.asyncio
async def test_get_reservation_by_id_raise_no_result_found_error(
    reservation_controller: ReservationController, app: FastAPI, client: TestClient
):
    _id = uuid.uuid4()

    def _mock_get_reservation_by_id():
        reservation_controller.get_reservation_by_id = AsyncMock(
            side_effect=ReservationNotFoundError(reservation_id=_id)
        )
        return reservation_controller

    app.dependency_overrides[get_reservation_controller] = _mock_get_reservation_by_id

    get_reservation_by_id_response = client.get(f"/reservations/{_id}")
    assert get_reservation_by_id_response.status_code == 404
    assert get_reservation_by_id_response.json() == {
        "message": f"Reservation with ID {_id} not found",
        "name": "ReservationNotFoundError",
        "status_code": 404,
    }


@pytest.mark.asyncio
async def test_get_reservations(
    reservation_controller: ReservationController, app: FastAPI, client: TestClient
):
    mock_reservations = [
        Reservation(
            id=uuid.uuid4(),
            created_at=datetime(2020, 1, 1),
            reservation_category=ReservationCategory("SIMPLE"),
            name="wwwwww",
            family_name="eeeee",
            amount_of_people=6,
            email_address="eeeee@admin.com",
            reservation_time=datetime(2020, 3, 3, 21, 30, 0),
            phone_number=PhoneNumber("+33633445566"),
        ),
        Reservation(
            id=uuid.uuid4(),
            created_at=datetime(2022, 2, 2),
            reservation_category=ReservationCategory("BIRTHDAY"),
            name="nnnnnn",
            family_name="bbbbb",
            amount_of_people=6,
            email_address="bbbbb@admin.com",
            reservation_time=datetime(2022, 2, 2, 22, 30, 0),
            phone_number=PhoneNumber("+336445566677"),
        ),
    ]

    def _mock_get_reservations():
        reservation_controller.get_reservations = AsyncMock(
            return_value=mock_reservations
        )
        return reservation_controller

    app.dependency_overrides[get_reservation_controller] = _mock_get_reservations

    get_reservations_response = client.get("/reservations")
    assert get_reservations_response.status_code == 200
    assert get_reservations_response.json() == [
        {
            "id": str(reservation.id),
            "created_at": reservation.created_at.isoformat(),
            "reservation_category": reservation.reservation_category.name,
            "name": reservation.name,
            "family_name": reservation.family_name,
            "amount_of_people": reservation.amount_of_people,
            "email_address": reservation.email_address,
            "reservation_time": reservation.reservation_time.isoformat(),
            "phone_number": str(reservation.phone_number),
        }
        for reservation in mock_reservations
    ]


@pytest.mark.asyncio
async def test_create_reservation(
    reservation_controller: ReservationController, app: FastAPI, client: TestClient
):
    reservation_data = {
        "reservation_category": "SIMPLE",
        "name": "aaaaaa",
        "family_name": "vvvvvv",
        "amount_of_people": 6,
        "email_address": "vvvvv@admin.com",
        "reservation_time": "2020-03-03T20:30:00",
        "phone_number": "+33633445566",
    }

    mock_reservation = Reservation(
        id=uuid.uuid4(),
        created_at=datetime(2020, 1, 1),
        reservation_category=ReservationCategory(
            reservation_data["reservation_category"]
        ),
        reservation_time=datetime.fromisoformat(reservation_data["reservation_time"]),
        **{
            k: v
            for k, v in reservation_data.items()
            if k not in ["reservation_category", "reservation_time"]
        },
    )

    def _mock_create_reservation():
        reservation_controller.create_reservation = AsyncMock(
            return_value=mock_reservation
        )
        return reservation_controller

    app.dependency_overrides[get_reservation_controller] = _mock_create_reservation

    create_reservation_response = client.post("/reservations", json=reservation_data)
    assert create_reservation_response.status_code == 201
    assert create_reservation_response.json() == {
        "id": str(mock_reservation.id),
        "created_at": mock_reservation.created_at.isoformat(),
        "reservation_category": mock_reservation.reservation_category.name,
        "name": mock_reservation.name,
        "family_name": mock_reservation.family_name,
        "amount_of_people": mock_reservation.amount_of_people,
        "email_address": mock_reservation.email_address,
        "reservation_time": mock_reservation.reservation_time.isoformat(),
        "phone_number": str(mock_reservation.phone_number),
    }


@pytest.mark.asyncio
async def test_update_reservation(
    reservation_controller: ReservationController, app: FastAPI, client: TestClient
):
    _id = uuid.uuid4()
    reservation_update_data = {
        "reservation_category": "SIMPLE",
        "name": "aaaaaa",
        "family_name": "vvvvvv",
        "amount_of_people": 6,
        "email_address": "vvvvv@admin.com",
        "reservation_time": "2020-03-03T20:30:00",
        "phone_number": "+33633445566",
    }

    updated_reservation = Reservation(
        id=_id,
        created_at=datetime(2020, 1, 1),
        reservation_category=ReservationCategory(
            reservation_update_data["reservation_category"]
        ),
        reservation_time=datetime.fromisoformat(
            reservation_update_data["reservation_time"]
        ),
        **{
            k: v
            for k, v in reservation_update_data.items()
            if k not in ["reservation_category", "reservation_time"]
        },
    )

    def _mock_update_reservation():
        reservation_controller.update_reservation = AsyncMock(
            return_value=updated_reservation
        )
        return reservation_controller

    app.dependency_overrides[get_reservation_controller] = _mock_update_reservation

    update_reservation_response = client.patch(
        f"/reservations/{_id}", json=reservation_update_data
    )
    assert update_reservation_response.status_code == 200
    assert update_reservation_response.json() == {
        "id": str(_id),
        "created_at": updated_reservation.created_at.isoformat(),
        "reservation_category": updated_reservation.reservation_category.name,
        "name": updated_reservation.name,
        "family_name": updated_reservation.family_name,
        "amount_of_people": updated_reservation.amount_of_people,
        "email_address": updated_reservation.email_address,
        "reservation_time": updated_reservation.reservation_time.isoformat(),
        "phone_number": str(updated_reservation.phone_number),
    }


@pytest.mark.asyncio
async def test_update_reservation_not_found_error(
    reservation_controller: ReservationController, client: TestClient, app: FastAPI
):
    _id = uuid.uuid4()

    reservation_update_data = {
        "reservation_category": "SIMPLE",
        "name": "UpdatedAaaaaa",
        "family_name": "vvvvvv",
        "amount_of_people": 6,
        "email_address": "vvvvv@admin.com",
        "reservation_time": "2020-03-03T20:30:00",
        "phone_number": "+33633445566",
    }

    def _mock_update_reservation():
        reservation_controller.update_reservation = AsyncMock(
            side_effect=ReservationNotFoundError(reservation_id=_id)
        )
        return reservation_controller

    app.dependency_overrides[get_reservation_controller] = _mock_update_reservation
    update_reservation_response = client.patch(
        f"/reservations/{_id}", json=reservation_update_data
    )
    assert update_reservation_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_reservation(
    reservation_controller: ReservationController, app: FastAPI, client: TestClient
):
    _id = uuid.uuid4()

    def _mock_delete_reservation():
        reservation_controller.delete_reservation = AsyncMock(return_value=None)
        return reservation_controller

    app.dependency_overrides[get_reservation_controller] = _mock_delete_reservation
    delete_reservation_response = client.delete(f"/reservations/{_id}")
    assert delete_reservation_response.status_code == 204


@pytest.mark.asyncio
async def test_delete_reservation_not_found_error(
    app: FastAPI, client: TestClient, reservation_controller: ReservationController
):
    _id = uuid.uuid4()

    def _mock_delete_reservation():
        reservation_controller.delete_reservation = AsyncMock(
            side_effect=ReservationNotFoundError(reservation_id=_id)
        )
        return reservation_controller

    app.dependency_overrides[get_reservation_controller] = _mock_delete_reservation
    delete_reservation_response = client.delete(f"/reservations/{_id}")
    assert delete_reservation_response.status_code == 404
