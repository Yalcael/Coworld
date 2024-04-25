from uuid import UUID
from fastapi import APIRouter, Depends
from typing import Sequence
from coworld.controllers.reservations import ReservationController
from coworld.dependencies import get_reservation_controller
from coworld.models.reservations import (
    Reservation,
    ReservationCreate,
    ReservationUpdate,
)

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Reservation])
async def get_reservations(
    *,
    reservation_controller: ReservationController = Depends(get_reservation_controller)
) -> Sequence[Reservation]:
    return await reservation_controller.get_reservations()


@router.get("/{reservation_id}", response_model=Reservation)
async def get_reservation_by_id(
    *,
    reservation_id: UUID,
    dish_controller: ReservationController = Depends(get_reservation_controller)
) -> Reservation:
    return await dish_controller.get_reservation_by_id(reservation_id)


@router.post("/", response_model=Reservation, status_code=201)
async def create_reservation(
    *,
    reservation_create: ReservationCreate,
    reservation_controller: ReservationController = Depends(get_reservation_controller)
) -> Reservation:
    return await reservation_controller.create_reservation(reservation_create)


@router.delete("/{reservation_id}", status_code=204)
async def delete_reservation(
    *,
    reservation_id: UUID,
    reservation_controller: ReservationController = Depends(get_reservation_controller)
) -> None:
    await reservation_controller.delete_reservation(reservation_id)


@router.patch("/{reservation_id}", response_model=Reservation)
async def update_reservation(
    *,
    reservation_id: UUID,
    reservation_update: ReservationUpdate,
    reservation_controller: ReservationController = Depends(get_reservation_controller)
) -> Reservation:
    return await reservation_controller.update_reservation(
        reservation_id, reservation_update
    )
