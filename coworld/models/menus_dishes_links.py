from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field


class MenuDishesLinksBase(SQLModel):
    dish_id: UUID
    menu_id: UUID


class MenuDishLinks(MenuDishesLinksBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())


class MenuDishLinksCreate(MenuDishesLinksBase):
    pass


class MenuDishLinksUpdate(MenuDishesLinksBase):
    pass
