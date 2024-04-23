from fastapi import APIRouter, Depends

from coworld.controllers.dishes import DishController
from coworld.dependencies import get_dish_controller
from coworld.models.dishes import DishCreate, Dish

router = APIRouter(
    prefix="/dishes",
    tags=["dishes"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Dish)
async def create_dish(*, dish_create: DishCreate, dish_controller: DishController = Depends(get_dish_controller)):
    return Dish.from_orm(await dish_controller.create_dish(dish_create))


@router.get("/", response_model=list[Dish])
async def get_dishes(*, dish_controller: DishController = Depends(get_dish_controller)):
    return [Dish.from_orm(dish) for dish in await dish_controller.get_dishes()]
