from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field


class MenuDishLinks(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    dish_id: UUID = Field(default=None, foreign_key="dish_id")
    menu_id: UUID = Field(default=None, foreign_key="menu.id")
