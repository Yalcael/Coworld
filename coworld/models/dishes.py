from uuid import UUID, uuid4
from datetime import datetime
from pydantic import PositiveFloat
from sqlmodel import Field, SQLModel
from enum import Enum


class Category(str, Enum):
    PLATS: str = 'PLATS'
    DRINKS: str = 'DRINKS'
    ENTRIES: str = 'ENTRIES'
    SAUCES: str = 'SAUCES'
    DESSERTS: str = 'DESSERTS'


class DishBase(SQLModel):
    category: Category
    title: str = Field(unique=True, index=True)
    ingredients: str
    description: str
    price: PositiveFloat


class Dish(DishBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())


class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    price: PositiveFloat | None = None
    category: Category | None = None
    title: str | None = None
    ingredients: str | None = None
    description: str | None = None
