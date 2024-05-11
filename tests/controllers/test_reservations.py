import pytest
import random
from faker import Faker
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import Session, select

from coworld.controllers.reservations import ReservationController
from coworld.models.errors import ReservationNotFoundError
from coworld.models.reservations import (
    ReservationCreate,
    ReservationCategory,
    Reservation,
    ReservationUpdate,
)


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
        phone_number=PhoneNumber("+33611223344"),
        reservation_time=faker.date_time(),
    )
    # Act
    result = await reservation_controller.create_reservation(reservation_create)

    reservation = session.exec(
        select(Reservation).where(Reservation.id == result.id)
    ).one()

    # Assert
    assert (
        result.reservation_category
        == reservation_create.reservation_category
        == reservation.reservation_category
    )
    assert result.name == reservation_create.name == reservation.name
    assert (
        result.family_name == reservation_create.family_name == reservation.family_name
    )
    assert (
        result.amount_of_people
        == reservation_create.amount_of_people
        == reservation.amount_of_people
    )
    assert (
        result.email_address
        == reservation_create.email_address
        == reservation.email_address
    )
    assert (
        result.phone_number
        == reservation_create.phone_number
        == reservation.phone_number
    )
    assert (
        result.reservation_time
        == reservation_create.reservation_time
        == reservation.reservation_time
    )


@pytest.mark.asyncio
async def test_get_reservations(
    reservation_controller: ReservationController, faker: Faker
) -> None:
    # Prepare
    number_reservations = 5
    created_reservations = []
    for _ in range(number_reservations):
        reservation_create = ReservationCreate(
            reservation_category=random.choice(list(ReservationCategory)),
            name=faker.name(),
            family_name=faker.name(),
            amount_of_people=random.randint(0, 100),
            email_address=faker.email(),
            phone_number=PhoneNumber("+33611223344"),
            reservation_time=faker.date_time(),
        )
        created_reservation = await reservation_controller.create_reservation(
            reservation_create
        )
        created_reservations.append(created_reservation)

    # Act
    all_reservations = await reservation_controller.get_reservations()

    # Assert
    assert len(all_reservations) == number_reservations
    for i, created_reservation in enumerate(created_reservations):
        assert (
            all_reservations[i].reservation_category
            == created_reservation.reservation_category
        )
        assert all_reservations[i].name == created_reservation.name
        assert all_reservations[i].family_name == created_reservation.family_name
        assert (
            all_reservations[i].amount_of_people == created_reservation.amount_of_people
        )
        assert all_reservations[i].email_address == created_reservation.email_address
        assert all_reservations[i].phone_number == created_reservation.phone_number
        assert (
            all_reservations[i].reservation_time == created_reservation.reservation_time
        )


@pytest.mark.asyncio
async def test_get_reservation_by_id(
    reservation_controller: ReservationController, faker: Faker
) -> None:
    # Prepare
    reservation_create = ReservationCreate(
        reservation_category=random.choice(list(ReservationCategory)),
        name=faker.name(),
        family_name=faker.name(),
        amount_of_people=random.randint(0, 100),
        email_address=faker.email(),
        phone_number=PhoneNumber("+33611223344"),
        reservation_time=faker.date_time(),
    )
    created_reservation = await reservation_controller.create_reservation(
        reservation_create
    )

    # Act
    retrieved_reservation = await reservation_controller.get_reservation_by_id(
        created_reservation.id
    )

    # Assert
    assert (
        retrieved_reservation.reservation_category
        == reservation_create.reservation_category
    )
    assert retrieved_reservation.name == reservation_create.name
    assert retrieved_reservation.family_name == reservation_create.family_name
    assert retrieved_reservation.amount_of_people == reservation_create.amount_of_people
    assert retrieved_reservation.email_address == reservation_create.email_address
    assert retrieved_reservation.phone_number == reservation_create.phone_number
    assert retrieved_reservation.reservation_time == reservation_create.reservation_time


@pytest.mark.asyncio
async def test_get_reservation_by_id_not_found(
    reservation_controller: ReservationController, faker: Faker
) -> None:
    # Prepare
    nonexistent_id = faker.uuid4()

    # Act and Assert
    with pytest.raises(ReservationNotFoundError):
        await reservation_controller.get_reservation_by_id(nonexistent_id)


@pytest.mark.asyncio
async def test_update_reservation(
    reservation_controller: ReservationController, faker: Faker
) -> None:
    # Prepare
    reservation_create = ReservationCreate(
        reservation_category=random.choice(list(ReservationCategory)),
        name=faker.name(),
        family_name=faker.name(),
        amount_of_people=random.randint(0, 100),
        email_address=faker.email(),
        phone_number=PhoneNumber("+33611223344"),
        reservation_time=faker.date_time(),
    )
    new_reservation = await reservation_controller.create_reservation(
        reservation_create
    )

    reservation_update = ReservationUpdate(
        reservation_category=random.choice(list(ReservationCategory)),
        name=faker.name(),
        family_name=faker.name(),
        amount_of_people=random.randint(0, 100),
        email_address=faker.email(),
        phone_number=PhoneNumber("+33611223388"),
        reservation_time=faker.date_time(),
    )
    # Act
    updated_reservation = await reservation_controller.update_reservation(
        new_reservation.id, reservation_update
    )

    # Assert
    assert (
        updated_reservation.reservation_category
        == reservation_update.reservation_category
    )
    assert updated_reservation.name == reservation_update.name
    assert updated_reservation.family_name == reservation_update.family_name
    assert updated_reservation.amount_of_people == reservation_update.amount_of_people
    assert updated_reservation.email_address == reservation_update.email_address
    assert updated_reservation.phone_number == reservation_update.phone_number
    assert updated_reservation.reservation_time == reservation_update.reservation_time


@pytest.mark.asyncio
async def test_update_reservation_not_found(
    reservation_controller: ReservationController, faker: Faker
) -> None:
    # Prepare
    reservation_update = ReservationUpdate(
        reservation_category=random.choice(list(ReservationCategory)),
        name=faker.name(),
        family_name=faker.name(),
        amount_of_people=random.randint(0, 100),
        email_address=faker.email(),
        phone_number=PhoneNumber("+33611223377"),
        reservation_time=faker.date_time(),
    )
    nonexistent_id = faker.uuid4()

    # Act and Assert
    with pytest.raises(ReservationNotFoundError):
        await reservation_controller.update_reservation(
            nonexistent_id, reservation_update
        )


@pytest.mark.asyncio
async def test_delete_reservation(
    reservation_controller: ReservationController, faker: Faker
) -> None:
    # Prepare
    reservation_create = ReservationCreate(
        reservation_category=random.choice(list(ReservationCategory)),
        name=faker.name(),
        family_name=faker.name(),
        amount_of_people=random.randint(0, 100),
        email_address=faker.email(),
        phone_number=PhoneNumber("+33611223344"),
        reservation_time=faker.date_time(),
    )
    new_reservation = await reservation_controller.create_reservation(
        reservation_create
    )

    # Act
    await reservation_controller.delete_reservation(new_reservation.id)

    # Assert
    with pytest.raises(ReservationNotFoundError):
        await reservation_controller.get_reservation_by_id(new_reservation.id)


@pytest.mark.asyncio
async def test_delete_reservation_not_found_error(
    reservation_controller: ReservationController, faker: Faker
) -> None:
    # Prepare
    nonexistent_id = faker.uuid4()

    # Act and Assert
    with pytest.raises(ReservationNotFoundError):
        await reservation_controller.delete_reservation(nonexistent_id)
