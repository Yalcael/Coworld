from uuid import UUID, uuid4
from datetime import datetime
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, AutoString
from enum import Enum


class ReservationCategory(Enum):
    BIRTHDAY = "BIRTHDAY"
    SIMPLE = "SIMPLE"


class ReservationBase(SQLModel):
    reservation_category: ReservationCategory
    name: str
    family_name: str
    amount_of_people: int
    email_address: EmailStr = Field(index=True, sa_type=AutoString)
    reservation_time: datetime
    phone_number: PhoneNumber = Field(index=True, sa_type=AutoString)


class Reservation(ReservationBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(SQLModel):
    reservation_category: ReservationCategory | None = None
    name: str | None = None
    family_name: str | None = None
    amount_of_people: int | None = None
    email_address: EmailStr | None = None
    reservation_time: datetime | None = None
    phone_number: PhoneNumber | None = None
