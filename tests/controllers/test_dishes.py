import random
import pytest
from faker import Faker
from sqlmodel import Session, select

from coworld.controllers.dishes import DishController
from coworld.models.dishes import DishCreate, Category
from coworld.models.models import Dish


@pytest.mark.asyncio
async def test_create_dish(
    dish_controller: DishController, session: Session, faker: Faker
) -> None:
    dish_create = DishCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        category=random.choice(list(Category)),
        ingredients=faker.text(max_nb_chars=24),
        price=random.uniform(0.99, 99.99),
        halal=random.choice([True, False]),
    )
    result = await dish_controller.create_dish(dish_create)
    dish = session.exec(select(Dish).where(Dish.id == result.id)).one()

    assert result.title == dish_create.title == dish.title
    assert result.description == dish_create.description == dish.description
    assert result.category == dish_create.category == dish.category
    assert result.ingredients == dish_create.ingredients == dish.ingredients
    assert result.price == dish_create.price == dish.price
    assert result.halal == dish_create.halal == dish.halal


@pytest.mark.asyncio
async def test_get_dish_by_id(dish_controller: DishController, faker: Faker) -> None:
    dish_create = DishCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        category=random.choice(list(Category)),
        ingredients=faker.text(max_nb_chars=24),
        price=random.uniform(0.99, 99.99),
        halal=random.choice([True, False]),
    )
    created_dish = await dish_controller.create_dish(dish_create)
    retrieved_dish = await dish_controller.get_dish_by_id(created_dish.id)

    assert retrieved_dish.title == dish_create.title
    assert retrieved_dish.description == dish_create.description
    assert retrieved_dish.category == dish_create.category
    assert retrieved_dish.ingredients == dish_create.ingredients
    assert retrieved_dish.price == dish_create.price
    assert retrieved_dish.halal == dish_create.halal


@pytest.mark.asyncio
async def test_get_dishes(dish_controller: DishController, faker: Faker) -> None:
    # Prepare
    number_dishes = 5
    created_dishes = []
    for _ in range(number_dishes):
        dish_create = DishCreate(
            title=faker.text(max_nb_chars=12),
            description=faker.text(max_nb_chars=24),
            category=random.choice(list(Category)),
            ingredients=faker.text(max_nb_chars=24),
            price=random.uniform(0.99, 99.99),
            halal=random.choice([True, False]),
        )
        created_dish = await dish_controller.create_dish(dish_create)
        created_dishes.append(created_dish)

    # Act
    all_dishes = await dish_controller.get_dishes()

    # Assert
    assert len(all_dishes) == number_dishes

    for i, created_dish in enumerate(created_dishes):
        assert all_dishes[i].title == created_dish.title
        assert all_dishes[i].description == created_dish.description
        assert all_dishes[i].category == created_dish.category
        assert all_dishes[i].ingredients == created_dish.ingredients
        assert all_dishes[i].price == created_dish.price
        assert all_dishes[i].halal == created_dish.halal
