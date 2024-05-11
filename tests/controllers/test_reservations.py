import pytest
import random
from faker import Faker
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import Session, select

from coworld.controllers.reservations import ReservationController
from coworld.models.reservations import (
    ReservationCreate,
    ReservationCategory,
    Reservation,
)


def generate_french_phone_number():
    # Randomly select either "+336" or "+337" as the prefix
    prefix = random.choice(["+336", "+337"])
    # Generate the remaining 8 digits
    remaining_digits = ''.join(str(random.randint(0, 9)) for _ in range(8))
    # Concatenate the prefix and remaining digits to form the phone number
    return PhoneNumber(f"{prefix}{remaining_digits}")


@pytest.mark.asyncio
async def test_create_reservation(
    reservation_controller: ReservationController, session: Session, faker: Faker
) -> None:
    # Prepare
    reservation_create = ReservationCreate(
        reservation_category=random.choice(list(ReservationCategory)),
        name=faker.name(),
        family_name=faker.name(),
        amount_of_people=random.randint(0, 100),
        email_address=faker.email(),
        phone_number=generate_french_phone_number(),
        reservation_time=faker.date_time(),
    )
    # Act
    result = await reservation_controller.create_reservation(reservation_create)

    reservation = session.exec(select(Reservation).where(Reservation.id == result.id)).one()

    # Assert
    assert result.reservation_category == reservation_create.reservation_category == reservation.reservation_category
    assert result.name == reservation_create.name == reservation.name
    assert result.family_name == reservation_create.family_name == reservation.family_name
    assert result.amount_of_people == reservation_create.amount_of_people == reservation.amount_of_people
    assert result.email_address == reservation_create.email_address == reservation.email_address
    assert result.phone_number == reservation_create.phone_number == reservation.phone_number
    assert result.reservation_time == reservation_create.reservation_time == reservation.reservation_time
