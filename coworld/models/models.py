from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from coworld.models.dishes import DishBase
from coworld.models.menus import MenuBase
from coworld.models.menus_dishes_links import MenuDishLinks


class Menu(MenuBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    dishes: list["Dish"] = Relationship(
        back_populates="menus", link_model=MenuDishLinks
    )


class Dish(DishBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    menus: list["Menu"] = Relationship(
        back_populates="dishes", link_model=MenuDishLinks
    )


class DishInMenu(DishBase):
    id: UUID
    created_at: datetime
    menus: list["Menu"] | None = None


class MenuWithDishes(MenuBase):
    id: UUID
    created_at: datetime
    dishes: list["Dish"] = []
