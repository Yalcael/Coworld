from pydantic import PositiveFloat
from sqlmodel import Field, SQLModel
from enum import Enum


class Category(str, Enum):
    PLATS: str = "PLATS"
    DRINKS: str = "DRINKS"
    ENTRIES: str = "ENTRIES"
    SAUCES: str = "SAUCES"
    DESSERTS: str = "DESSERTS"


class DishBase(SQLModel):
    category: Category
    title: str = Field(unique=True, index=True)
    ingredients: str
    description: str
    price: PositiveFloat


class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    price: PositiveFloat | None = None
    category: Category | None = None
    title: str | None = None
    ingredients: str | None = None
    description: str | None = None
