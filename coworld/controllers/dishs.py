from coworld.models.dishes import Dish, DishCreate, DishUpdate
from uuid import UUID
from sqlmodel import Session, select


class DishController:
    def __init__(self, session: Session):
        self.session = session

    async def get_dishes(self) -> list[Dish]:
        return self.session.exec(select(Dish)).all()

    async def get_dish_by_id(self, dish_id: UUID) -> Dish:
        return self.session.exec(select(Dish).where(Dish.id == dish_id)).one()

    async def create_dish(self, dish_create: DishCreate) -> Dish:
        new_dish = Dish(**dish_create.dict())
        self.session.add(new_dish)
        self.session.commit()
        self.session.refresh(new_dish)
        return new_dish

    async def delete_dish(self, dish_id: UUID) -> None:
        dish = self.session.exec(select(Dish).where(Dish.id == dish_id)).one()
        self.session.delete(dish)
        self.session.commit()

    async def update_dish(self, dish_id: UUID, dish_update: DishUpdate) -> Dish:
        dish = self.session.exec(select(Dish).where(Dish.id == dish_id)).one()
        for key, value in dish_update.dict(exclude_unset=True).items():
            setattr(dish, key, value)
        self.session.add(dish)
        self.session.commit()
        self.session.refresh(dish)
        return dish
