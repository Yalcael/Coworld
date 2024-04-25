from uuid import UUID, uuid4
from datetime import datetime
from pydantic import PositiveFloat
from sqlmodel import Field, SQLModel


class MenuBase(SQLModel):
    title: str = Field(unique=True, index=True)
    description: str
    price: PositiveFloat


class Menu(MenuBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    price: PositiveFloat | None = None
    title: str | None = None
    description: str | None = None
