from typing import Sequence
from coworld.models.dishes import DishCreate, DishUpdate, Category
from coworld.models.models import Dish
from coworld.models.errors import DishNotFoundError, DishAlreadyExistsError
from uuid import UUID
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, select


class DishController:
    def __init__(self, session: Session):
        self.session = session

    async def get_dishes(self) -> Sequence[Dish]:
        return self.session.exec(select(Dish)).all()

    async def get_dish_by_id(self, dish_id: UUID) -> Dish:
        try:
            return self.session.exec(select(Dish).where(Dish.id == dish_id)).one()
        except NoResultFound:
            raise DishNotFoundError(dish_id=dish_id)

    async def create_dish(self, dish_create: DishCreate) -> Dish:
        try:
            new_dish = Dish(**dish_create.model_dump())
            self.session.add(new_dish)
            self.session.commit()
            self.session.refresh(new_dish)
            return new_dish
        except IntegrityError:
            raise DishAlreadyExistsError(title=dish_create.title)

    async def delete_dish(self, dish_id: UUID) -> None:
        try:
            dish = self.session.exec(select(Dish).where(Dish.id == dish_id)).one()
            self.session.delete(dish)
            self.session.commit()
        except NoResultFound:
            raise DishNotFoundError(dish_id=dish_id)

    async def update_dish(self, dish_id: UUID, dish_update: DishUpdate) -> Dish:
        try:
            dish = self.session.exec(select(Dish).where(Dish.id == dish_id)).one()
            for key, value in dish_update.dict(exclude_unset=True).items():
                setattr(dish, key, value)
            self.session.add(dish)
            self.session.commit()
            self.session.refresh(dish)
            return dish
        except NoResultFound:
            raise DishNotFoundError(dish_id=dish_id)

    async def get_halal_dishes(self, is_halal: bool) -> Sequence[Dish]:
        return self.session.exec(select(Dish).where(Dish.halal == is_halal)).all()

    async def get_dishes_by_category(self, dishes_category: Category) -> Sequence[Dish]:
        return self.session.exec(
            select(Dish).where(Dish.category == dishes_category)
        ).all()
