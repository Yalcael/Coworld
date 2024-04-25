from uuid import UUID, uuid4
from datetime import datetime
import phonenumbers
from phonenumbers import PhoneNumber
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, AutoString
from enum import Enum


class ReservationCategory(Enum):
    BIRTHDAY = 'BIRTHDAY'
    SIMPLE = "SIMPLE"


def validate_french_phone_number(number: str) -> str:
    parsed_number = phonenumbers.parse(number, "FR")
    if not phonenumbers.is_valid_number(parsed_number):
        raise ValueError("Not a valid French phone number")
    return number


class ReservationBase(SQLModel):
    reservation_category: ReservationCategory
    name: str
    family_name: str
    amount_of_people: int
    email_address: EmailStr = Field(index=True, sa_type=AutoString)
    reservation_time: datetime
    phone_number: PhoneNumber = Field(index=True, sa_type=PhoneNumber)


class Reservation(ReservationBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(ReservationBase):
    pass
