from uuid import UUID
from fastapi import APIRouter, Depends
from typing import Sequence
from coworld.controllers.menus import MenuController
from coworld.dependencies import get_menu_controller
from coworld.models.menus import Menu, MenuCreate, MenuUpdate

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


@router.get("/", response_model=list[Menu])
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
