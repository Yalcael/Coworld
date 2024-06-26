from typing import Sequence
from uuid import UUID
from fastapi import APIRouter, Depends
from coworld.controllers.dishes import DishController
from coworld.dependencies import get_dish_controller
from coworld.models.dishes import DishCreate, DishUpdate, Category
from coworld.models.models import Dish, DishInMenu

router = APIRouter(
    prefix="/dishes",
    tags=["dishes"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Dish, status_code=201)
async def create_dish(
    *,
    dish_create: DishCreate,
    dish_controller: DishController = Depends(get_dish_controller)
) -> Dish:
    return await dish_controller.create_dish(dish_create)


@router.get("/", response_model=list[DishInMenu])
async def get_dishes(
    *, dish_controller: DishController = Depends(get_dish_controller)
) -> Sequence[Dish]:
    return await dish_controller.get_dishes()


@router.get("/{dish_id}", response_model=Dish)
async def get_dish_by_id(
    *, dish_id: UUID, dish_controller: DishController = Depends(get_dish_controller)
) -> Dish:
    return await dish_controller.get_dish_by_id(dish_id)


@router.delete("/{dish_id}", status_code=204)
async def delete_dish(
    *, dish_id: UUID, dish_controller: DishController = Depends(get_dish_controller)
) -> None:
    await dish_controller.delete_dish(dish_id)


@router.patch("/{dish_id}", response_model=Dish)
async def update_dish(
    *,
    dish_id: UUID,
    dish_update: DishUpdate,
    dish_controller: DishController = Depends(get_dish_controller)
) -> Dish:
    return await dish_controller.update_dish(dish_id, dish_update)


@router.get("/type/halal", response_model=list[Dish])
async def get_halal_dishes(
    *, is_halal: bool, dish_controller: DishController = Depends(get_dish_controller)
) -> Sequence[Dish]:
    return await dish_controller.get_halal_dishes(is_halal)


@router.get("/type/category", response_model=list[Dish])
async def get_dishes_by_category(
    category: Category, dish_controller: DishController = Depends(get_dish_controller)
) -> Sequence[Dish]:
    return await dish_controller.get_dishes_by_category(category)
