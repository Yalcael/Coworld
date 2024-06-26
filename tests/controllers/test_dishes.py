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
    list_category = list(Category)
    list_of_dishes = []
    for category in list_category:
        dish_create = DishCreate(
            title=faker.text(max_nb_chars=12),
            description=faker.text(max_nb_chars=24),
            category=Category(category),
            ingredients=faker.text(max_nb_chars=24),
            price=random.uniform(0.99, 99.99),
            halal=random.choice([True, False]),
        )
        list_of_dishes.append(await dish_controller.create_dish(dish_create))
    random_category = random.choice(list_category)
    dish_create_2 = DishCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        category=random_category,
        ingredients=faker.text(max_nb_chars=24),
        price=random.uniform(0.99, 99.99),
        halal=random.choice([True, False]),
    )
    list_of_dishes.append(await dish_controller.create_dish(dish_create_2))

    # Act
    dishes_by_category = await dish_controller.get_dishes_by_category(random_category)
    list_of_dishes = list(
        filter(lambda dish: dish.category == random_category, dishes_by_category)
    )

    # Assert
    assert list_of_dishes[0] == dishes_by_category[0]
    assert list_of_dishes[1] == dishes_by_category[1]


@pytest.mark.asyncio
async def test_get_halal_dishes(dish_controller: DishController, faker: Faker) -> None:
    # Prepare
    halal_dishes = []
    non_halal_dishes = []

    # Create halal and non-halal dishes
    for _ in range(5):
        dish_create_halal = DishCreate(
            title=faker.text(max_nb_chars=12),
            description=faker.text(max_nb_chars=24),
            category=random.choice(list(Category)),
            ingredients=faker.text(max_nb_chars=24),
            price=random.uniform(0.99, 99.99),
            halal=True,
        )
        dish_create_non_halal = DishCreate(
            title=faker.text(max_nb_chars=12),
            description=faker.text(max_nb_chars=24),
            category=random.choice(list(Category)),
            ingredients=faker.text(max_nb_chars=24),
            price=random.uniform(0.99, 99.99),
            halal=False,
        )
        halal_dishes.append(await dish_controller.create_dish(dish_create_halal))
        non_halal_dishes.append(
            await dish_controller.create_dish(dish_create_non_halal)
        )

    # Act
    halal_result = await dish_controller.get_halal_dishes(is_halal=True)
    non_halal_result = await dish_controller.get_halal_dishes(is_halal=False)

    # Assert
    assert len(halal_result) == len(halal_dishes)
    assert all(dish.halal for dish in halal_result)

    assert len(non_halal_result) == len(non_halal_dishes)
    assert not any(dish.halal for dish in non_halal_result)
