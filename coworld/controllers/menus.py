from typing import Sequence

from coworld.models.menus import MenuCreate, MenuUpdate
from coworld.models.models import Menu, Dish
from coworld.models.errors import (
    MenuNotFoundError,
    MenuAlreadyExistsError,
    DishInMenuNotFoundError,
    DishAlreadyInMenuError,
)
from uuid import UUID
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, select

from coworld.models.menus_dishes_links import MenuDishLinksCreate, MenuDishLinks


class MenuController:
    def __init__(self, session: Session):
        self.session = session

    async def get_menus(self) -> Sequence[Menu]:
        return self.session.exec(select(Menu)).all()

    async def create_menu(self, menu_create: MenuCreate) -> Menu:
        try:
            new_menu = Menu(**menu_create.dict())
            self.session.add(new_menu)
            self.session.commit()
            self.session.refresh(new_menu)
            return new_menu
        except IntegrityError:
            raise MenuAlreadyExistsError(title=menu_create.title)

    async def get_menu_by_id(self, menu_id: UUID) -> Menu:
        try:
            return self.session.exec(select(Menu).where(Menu.id == menu_id)).one()
        except NoResultFound:
            raise MenuNotFoundError(menu_id=menu_id)

    async def delete_menu(self, menu_id: UUID) -> None:
        try:
            menu = self.session.exec(select(Menu).where(Menu.id == menu_id)).one()
            self.session.delete(menu)
            self.session.commit()
        except NoResultFound:
            raise MenuNotFoundError(menu_id=menu_id)

    async def update_menu(self, menu_id: UUID, menu_update: MenuUpdate) -> Menu:
        try:
            menu = self.session.exec(select(Menu).where(Menu.id == menu_id)).one()
            for key, value in menu_update.dict(exclude_unset=True).items():
                setattr(menu, key, value)
            self.session.add(menu)
            self.session.commit()
            self.session.refresh(menu)
            return menu
        except NoResultFound:
            raise MenuNotFoundError(menu_id=menu_id)

    async def add_dish_to_menu(
        self, menu_dish_links_create: MenuDishLinksCreate
    ) -> Menu:
        try:
            menu = self.session.exec(
                select(Menu).where(Menu.id == menu_dish_links_create.menu_id)
            ).one()
            for dish_id in menu_dish_links_create.dish_ids:
                dish = self.session.exec(select(Dish).where(Dish.id == dish_id)).one()
                menu_dish_links = MenuDishLinks(
                    dish_id=dish_id, menu_id=menu_dish_links_create.menu_id
                )
                self.session.add(menu_dish_links)
            self.session.commit()
            self.session.refresh(menu)
            return menu
        except NoResultFound:
            raise MenuNotFoundError(menu_id=menu_dish_links_create.menu_id)
        except IntegrityError:
            self.session.rollback()
            raise DishAlreadyInMenuError(
                dish=dish.title, menu_id=menu_dish_links_create.menu_id
            )

    async def delete_dish_from_menu(self, menu_id: UUID, dish_id: UUID) -> None:
        try:
            menu_dish_link = self.session.exec(
                select(MenuDishLinks)
                .where(MenuDishLinks.menu_id == menu_id)
                .where(MenuDishLinks.dish_id == dish_id)
            ).one()
            self.session.delete(menu_dish_link)
            self.session.commit()
        except NoResultFound:
            raise DishInMenuNotFoundError(menu_id=menu_id, dish_id=dish_id)

    async def get_discounted_menus(self) -> Sequence[Menu]:
        return self.session.exec(select(Menu).where(Menu.discount > 0)).all()
