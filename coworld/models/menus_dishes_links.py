from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel, Field


class MenuDishesLinksBase(SQLModel):
    dish_id: UUID
    menu_id: UUID


class MenuDishLinks(MenuDishesLinksBase, table=True):
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    dish_id: UUID = Field(foreign_key="dish.id", primary_key=True)
    menu_id: UUID = Field(foreign_key="menu.id", primary_key=True)


class MenuDishLinksCreate(SQLModel):
    dish_ids: list[UUID]


class MenuDishLinksUpdate(SQLModel):
    pass
