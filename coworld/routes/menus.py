from uuid import UUID
from fastapi import APIRouter, Depends
from typing import Sequence
from coworld.controllers.menus import MenuController
from coworld.dependencies import get_menu_controller
from coworld.models.menus import MenuCreate, MenuUpdate
from coworld.models.models import Menu, MenuWithDishes
from coworld.models.menus_dishes_links import MenuDishLinksCreate

router = APIRouter(
    prefix="/menus",
    tags=["menus"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Menu, status_code=201)
async def create_menu(
    *,
    menu_create: MenuCreate,
    menu_controller: MenuController = Depends(get_menu_controller)
) -> Menu:
    return await menu_controller.create_menu(menu_create)


@router.get("/", response_model=list[MenuWithDishes])
async def get_menus(
    *, menu_controller: MenuController = Depends(get_menu_controller)
) -> Sequence[Menu]:
    return await menu_controller.get_menus()


@router.get("/{menu_id}", response_model=Menu)
async def get_menu_by_id(
    *, menu_id: UUID, menu_controller: MenuController = Depends(get_menu_controller)
) -> Menu:
    return await menu_controller.get_menu_by_id(menu_id)


@router.delete("/{menu_id}", status_code=204)
async def delete_menu(
    *, menu_id: UUID, menu_controller: MenuController = Depends(get_menu_controller)
) -> None:
    await menu_controller.delete_menu(menu_id)


@router.patch("/{menu_id}", response_model=Menu)
async def update_menu(
    *,
    menu_id: UUID,
    menu_update: MenuUpdate,
    menu_controller: MenuController = Depends(get_menu_controller)
) -> Menu:
    return await menu_controller.update_menu(menu_id, menu_update)


@router.patch("/{menu_id}/link_dish", response_model=Menu, status_code=200)
async def add_dish_to_menu(
    *,
    menu_id: UUID,
    menu_dish_links_create: MenuDishLinksCreate,
    menu_controller: MenuController = Depends(get_menu_controller)
) -> Menu:
    return await menu_controller.add_dish_to_menu(menu_id, menu_dish_links_create)


@router.delete("/{menu_id}/unlink_dish/{dish_id}", status_code=204)
async def delete_dish_from_menu(
    *,
    menu_id: UUID,
    dish_id: UUID,
    menu_controller: MenuController = Depends(get_menu_controller)
) -> None:
    await menu_controller.delete_dish_from_menu(menu_id, dish_id)
