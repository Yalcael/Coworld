from pydantic import PositiveFloat
from sqlmodel import Field, SQLModel


class MenuBase(SQLModel):
    title: str = Field(unique=True, index=True)
    description: str
    price: PositiveFloat


class MenuCreate(MenuBase):
    pass


class MenuUpdate(SQLModel):
    price: PositiveFloat | None = None
    title: str | None = None
    description: str | None = None
