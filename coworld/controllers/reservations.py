from typing import Sequence
from uuid import UUID

from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from coworld.models.errors import ReservationNotFoundError
from coworld.models.reservations import (
    Reservation,
    ReservationCreate,
    ReservationUpdate,
)


class ReservationController:
    def __init__(self, session: Session):
        self.session = session

    async def get_reservations(self) -> Sequence[Reservation]:
        return self.session.exec(select(Reservation)).all()

    async def get_reservation_by_id(self, reservation_id: UUID) -> Reservation:
        try:
            return self.session.exec(
                select(Reservation).where(Reservation.id == reservation_id)
            ).one()
        except NoResultFound:
            raise ReservationNotFoundError(reservation_id=reservation_id)

    async def create_reservation(
        self, reservation_create: ReservationCreate
    ) -> Reservation:
        new_reservation = Reservation(**reservation_create.dict())
        self.session.add(new_reservation)
        self.session.commit()
        self.session.refresh(new_reservation)
        return new_reservation

    async def delete_reservation(self, reservation_id: UUID) -> None:
        try:
            reservation = self.session.exec(
                select(Reservation).where(Reservation.id == reservation_id)
            ).one()
            self.session.delete(reservation)
            self.session.commit()
        except NoResultFound:
            raise ReservationNotFoundError(reservation_id=reservation_id)

    async def update_reservation(
        self, reservation_id: UUID, reservation_update: ReservationUpdate
    ) -> Reservation:
        try:
            reservation = self.session.exec(
                select(Reservation).where(Reservation.id == reservation_id)
            ).one()
            for key, value in reservation_update.dict(exclude_unset=True).items():
                setattr(reservation, key, value)
            self.session.add(reservation)
            self.session.commit()
            self.session.refresh(reservation)
            return reservation
        except NoResultFound:
            raise ReservationNotFoundError(reservation_id=reservation_id)
