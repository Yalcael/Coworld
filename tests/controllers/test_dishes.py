import random

import pytest
from faker import Faker
from sqlmodel import Session, select

from coworld.controllers.dishes import DishController
from coworld.models.dishes import DishCreate, Category, DishUpdate
from coworld.models.errors import DishNotFoundError, DishAlreadyExistsError
from coworld.models.models import Dish


@pytest.mark.asyncio
async def test_create_dish(
    dish_controller: DishController, session: Session, faker: Faker
) -> None:
    # Prepare
    dish_create = DishCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        category=random.choice(list(Category)),
        ingredients=faker.text(max_nb_chars=24),
        price=random.uniform(0.99, 99.99),
        halal=random.choice([True, False]),
    )
    # Act
    result = await dish_controller.create_dish(dish_create)

    dish = session.exec(select(Dish).where(Dish.id == result.id)).one()

    # Assert
    assert result.title == dish_create.title == dish.title
    assert result.description == dish_create.description == dish.description
    assert result.category == dish_create.category == dish.category
    assert result.ingredients == dish_create.ingredients == dish.ingredients
    assert result.price == dish_create.price == dish.price
    assert result.halal == dish_create.halal == dish.halal


@pytest.mark.asyncio
async def test_create_dish_already_exist(
    dish_controller: DishController, faker: Faker
) -> None:
    # Prepare

    dish_create = DishCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        category=random.choice(list(Category)),
        ingredients=faker.text(max_nb_chars=24),
        price=random.uniform(0.99, 99.99),
        halal=random.choice([True, False]),
    )
    await dish_controller.create_dish(dish_create)

    # Act / Assert
    with pytest.raises(DishAlreadyExistsError):
        await dish_controller.create_dish(dish_create)


@pytest.mark.asyncio
async def test_get_dish_by_id(dish_controller: DishController, faker: Faker) -> None:
    # Prepare
    dish_create = DishCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        category=random.choice(list(Category)),
        ingredients=faker.text(max_nb_chars=24),
        price=random.uniform(0.99, 99.99),
        halal=random.choice([True, False]),
    )
    created_dish = await dish_controller.create_dish(dish_create)

    # Act
    retrieved_dish = await dish_controller.get_dish_by_id(created_dish.id)

    # Assert
    assert retrieved_dish.title == dish_create.title
    assert retrieved_dish.description == dish_create.description
    assert retrieved_dish.category == dish_create.category
    assert retrieved_dish.ingredients == dish_create.ingredients
    assert retrieved_dish.price == dish_create.price
    assert retrieved_dish.halal == dish_create.halal


@pytest.mark.asyncio
async def test_get_dish_by_id_not_found_error(
    dish_controller: DishController, faker: Faker
) -> None:
    # Prepare
    non_existent_id = faker.uuid4()
    # Act and Assert
    with pytest.raises(DishNotFoundError):
        await dish_controller.get_dish_by_id(non_existent_id)


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


@pytest.mark.asyncio
async def test_update_dish(dish_controller: DishController, faker: Faker) -> None:
    # Prepare
    dish_create = DishCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        category=random.choice(list(Category)),
        ingredients=faker.text(max_nb_chars=24),
        price=random.uniform(0.99, 99.99),
        halal=random.choice([True, False]),
    )
    new_dish = await dish_controller.create_dish(dish_create)

    dish_update = DishUpdate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        category=random.choice(list(Category)),
        ingredients=faker.text(max_nb_chars=24),
        price=random.uniform(0.99, 99.99),
        halal=random.choice([True, False]),
    )
    # Act
    updated_dish = await dish_controller.update_dish(new_dish.id, dish_update)

    # Assert
    assert updated_dish.title == dish_update.title
    assert updated_dish.description == dish_update.description
    assert updated_dish.category == dish_update.category
    assert updated_dish.ingredients == dish_update.ingredients
    assert updated_dish.price == dish_update.price
    assert updated_dish.halal == dish_update.halal


@pytest.mark.asyncio
async def test_update_dish_not_found_error(
    dish_controller: DishController, faker: Faker
) -> None:
    # Prepare
    dish_update = DishUpdate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        category=random.choice(list(Category)),
        ingredients=faker.text(max_nb_chars=24),
        price=random.uniform(0.99, 99.99),
        halal=random.choice([True, False]),
    )
    nonexistent_id = faker.uuid4()

    # Act and Assert
    with pytest.raises(DishNotFoundError):
        await dish_controller.update_dish(nonexistent_id, dish_update)


@pytest.mark.asyncio
async def test_delete_dish(dish_controller: DishController, faker: Faker) -> None:
    # Prepare
    dish_create = DishCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        category=random.choice(list(Category)),
        ingredients=faker.text(max_nb_chars=24),
        price=random.uniform(0.99, 99.99),
        halal=random.choice([True, False]),
    )
    new_dish = await dish_controller.create_dish(dish_create)

    # Act
    await dish_controller.delete_dish(new_dish.id)

    # Assert
    with pytest.raises(DishNotFoundError):
        await dish_controller.get_dish_by_id(new_dish.id)


@pytest.mark.asyncio
async def test_delete_dish_not_found_error(
    dish_controller: DishController, faker: Faker
) -> None:
    # Prepare
    nonexistent_id = faker.uuid4()

    # Act and Assert
    with pytest.raises(DishNotFoundError):
        await dish_controller.delete_dish(nonexistent_id)


@pytest.mark.asyncio
async def test_get_dishes_by_category(
    dish_controller: DishController, faker: Faker
) -> None:
    # Prepare
    category = random.choice(list(Category))
    number_dishes = 5

    for _ in range(number_dishes):
        dish_create = DishCreate(
            title=faker.text(max_nb_chars=12),
            description=faker.text(max_nb_chars=24),
            category=category,
            ingredients=faker.text(max_nb_chars=24),
            price=random.uniform(0.99, 99.99),
            halal=random.choice([True, False]),
        )
        await dish_controller.create_dish(dish_create)

    # Act
    dishes_by_category = await dish_controller.get_dishes_by_category(category)

    # Assert
    assert dishes_by_category
    for dish in dishes_by_category:
        assert dish.category == category
        assert dish.title
        assert dish.description
        assert dish.ingredients
        assert 0.99 <= dish.price <= 99.99
        assert isinstance(dish.halal, bool)


@pytest.mark.asyncio
async def test_get_halal_dishes(dish_controller: DishController, faker: Faker) -> None:
    # Prepare
    number_dishes = 5

    for _ in range(number_dishes):
        dish_create = DishCreate(
            title=faker.text(max_nb_chars=12),
            description=faker.text(max_nb_chars=24),
            category=random.choice(list(Category)),
            ingredients=faker.text(max_nb_chars=24),
            price=random.uniform(0.99, 99.99),
            halal=True,
        )
        await dish_controller.create_dish(dish_create)

    for _ in range(number_dishes):
        dish_create = DishCreate(
            title=faker.text(max_nb_chars=12),
            description=faker.text(max_nb_chars=24),
            category=random.choice(list(Category)),
            ingredients=faker.text(max_nb_chars=24),
            price=random.uniform(0.99, 99.99),
            halal=False,
        )
        await dish_controller.create_dish(dish_create)

    # Act
    halal_dishes = await dish_controller.get_halal_dishes(is_halal=True)

    # Assert
    assert halal_dishes
    for dish in halal_dishes:
        assert dish.halal is True
        assert dish.title
        assert dish.category
        assert dish.description
        assert dish.ingredients
        assert 0.99 <= dish.price <= 99.99
