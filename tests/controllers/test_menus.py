from coworld.controllers.dishes import DishController
from coworld.controllers.menus import MenuController
import pytest
import random
from faker import Faker
from sqlmodel import Session, select

from coworld.models.dishes import DishCreate, Category
from coworld.models.errors import (
    MenuAlreadyExistsError,
    MenuNotFoundError,
    DishAlreadyInMenuError,
    DishInMenuNotFoundError,
)
from coworld.models.menus import MenuCreate, MenuUpdate
from coworld.models.menus_dishes_links import MenuDishLinksCreate
from coworld.models.models import Menu


@pytest.mark.asyncio
async def test_create_menu(
    menu_controller: MenuController, session: Session, faker: Faker
) -> None:
    # Prepare
    menu_create = MenuCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        price=random.uniform(2.99, 99.99),
        discount=random.randint(0, 100),
    )
    # Act
    result = await menu_controller.create_menu(menu_create)

    menu = session.exec(select(Menu).where(Menu.id == result.id)).one()

    # Assert
    assert result.title == menu_create.title == menu.title
    assert result.description == menu_create.description == menu.description
    assert result.price == menu_create.price == menu.price
    assert result.discount == menu_create.discount == menu.discount


@pytest.mark.asyncio
async def test_create_menu_already_exist_error(
    menu_controller: MenuController, faker: Faker
) -> None:
    # Prepare
    menu_create = MenuCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        price=random.uniform(2.99, 99.99),
        discount=random.randint(0, 100),
    )
    await menu_controller.create_menu(menu_create)

    # Act & Assert
    with pytest.raises(MenuAlreadyExistsError):
        await menu_controller.create_menu(menu_create)


@pytest.mark.asyncio
async def test_get_menu_by_id(menu_controller: MenuController, faker: Faker) -> None:
    # Prepare
    menu_create = MenuCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        price=random.uniform(2.99, 99.99),
        discount=random.randint(0, 100),
    )
    created_menu = await menu_controller.create_menu(menu_create)

    # Act
    retrieved_menu = await menu_controller.get_menu_by_id(created_menu.id)

    # Assert
    assert retrieved_menu.title == menu_create.title
    assert retrieved_menu.description == menu_create.description
    assert retrieved_menu.price == menu_create.price
    assert retrieved_menu.discount == menu_create.discount


@pytest.mark.asyncio
async def test_get_menu_by_id_not_found(
    menu_controller: MenuController, faker: Faker
) -> None:
    # Prepare
    nonexistent_id = faker.uuid4()

    # Act and Assert
    with pytest.raises(MenuNotFoundError):
        await menu_controller.get_menu_by_id(nonexistent_id)


@pytest.mark.asyncio
async def test_get_menus(menu_controller: MenuController, faker: Faker) -> None:
    # Prepare
    number_menus = 5
    created_menus = []
    for _ in range(number_menus):
        menu_create = MenuCreate(
            title=faker.text(max_nb_chars=12),
            description=faker.text(max_nb_chars=24),
            price=random.uniform(2.99, 99.99),
            discount=random.randint(0, 100),
        )
        created_menu = await menu_controller.create_menu(menu_create)
        created_menus.append(created_menu)

    # Act
    all_menus = await menu_controller.get_menus()

    # Assert
    assert len(all_menus) == number_menus

    for i, created_menu in enumerate(created_menus):
        assert all_menus[i].title == created_menu.title
        assert all_menus[i].description == created_menu.description
        assert all_menus[i].price == created_menu.price
        assert all_menus[i].discount == created_menu.discount


@pytest.mark.asyncio
async def test_update_menu(menu_controller: MenuController, faker: Faker) -> None:
    # Prepare
    menu_create = MenuCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        price=random.uniform(2.99, 99.99),
        discount=random.randint(0, 100),
    )
    new_menu = await menu_controller.create_menu(menu_create)

    menu_update = MenuUpdate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        price=random.uniform(2.99, 99.99),
        discount=random.randint(0, 100),
    )
    # Act
    updated_menu = await menu_controller.update_menu(new_menu.id, menu_update)

    # Assert
    assert updated_menu.title == menu_update.title
    assert updated_menu.description == menu_update.description
    assert updated_menu.price == menu_update.price
    assert updated_menu.discount == menu_update.discount


@pytest.mark.asyncio
async def test_update_menu_not_found(
    menu_controller: MenuController, faker: Faker
) -> None:
    # Prepare
    menu_update = MenuUpdate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        price=random.uniform(2.99, 99.99),
        discount=random.randint(0, 100),
    )
    nonexistent_id = faker.uuid4()

    # Act and Assert
    with pytest.raises(MenuNotFoundError):
        await menu_controller.update_menu(nonexistent_id, menu_update)


@pytest.mark.asyncio
async def test_delete_menu(menu_controller: MenuController, faker: Faker) -> None:
    # Prepare
    menu_create = MenuCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        price=random.uniform(2.99, 99.99),
        discount=random.randint(0, 100),
    )
    new_menu = await menu_controller.create_menu(menu_create)

    # Act
    await menu_controller.delete_menu(new_menu.id)

    # Assert
    with pytest.raises(MenuNotFoundError):
        await menu_controller.get_menu_by_id(new_menu.id)


@pytest.mark.asyncio
async def test_delete_menu_not_found_error(
    menu_controller: MenuController, faker: Faker
) -> None:
    # Prepare
    nonexistent_id = faker.uuid4()

    # Act and Assert
    with pytest.raises(MenuNotFoundError):
        await menu_controller.delete_menu(nonexistent_id)


@pytest.mark.asyncio
async def test_add_dish_to_menu(
    menu_controller: MenuController, dish_controller: DishController, faker: Faker
) -> None:
    # Prepare
    menu_create = MenuCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        price=random.uniform(2.99, 99.99),
        discount=random.randint(0, 100),
    )
    created_menu = await menu_controller.create_menu(menu_create)

    dish_create = DishCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        category=random.choice(list(Category)),
        ingredients=faker.text(max_nb_chars=24),
        price=random.uniform(0.99, 99.99),
        halal=random.choice([True, False]),
    )
    created_dish = await dish_controller.create_dish(dish_create)

    # Act: Link the dish to the menu
    menu_dish_links_create = MenuDishLinksCreate(
        dish_ids=[created_dish.id], menu_id=created_menu.id
    )
    updated_menu = await menu_controller.add_dish_to_menu(
        menu_id=created_menu.id, menu_dish_links_create=menu_dish_links_create
    )

    # Assert
    assert created_dish.id in [dish.id for dish in updated_menu.dishes]
    assert updated_menu.id == created_menu.id

    # Act again: Try to add the same dish to the menu
    with pytest.raises(DishAlreadyInMenuError):
        await menu_controller.add_dish_to_menu(
            menu_id=created_menu.id, menu_dish_links_create=menu_dish_links_create
        )


@pytest.mark.asyncio
async def test_add_dish_to_menu_with_nonexistent_menu(
    dish_controller: DishController, menu_controller: MenuController, faker: Faker
) -> None:
    # Prepare
    nonexistent_menu_id = faker.uuid4()

    dish_create = DishCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        category=random.choice(list(Category)),
        ingredients=faker.text(max_nb_chars=24),
        price=random.uniform(0.99, 99.99),
        halal=random.choice([True, False]),
    )
    created_dish = await dish_controller.create_dish(dish_create)

    menu_dish_links_create = MenuDishLinksCreate(
        dish_ids=[created_dish.id], menu_id=nonexistent_menu_id
    )

    # Act & Assert
    with pytest.raises(MenuNotFoundError):
        await menu_controller.add_dish_to_menu(
            menu_id=nonexistent_menu_id, menu_dish_links_create=menu_dish_links_create
        )


@pytest.mark.asyncio
async def test_delete_dish_from_menu(
    menu_controller: MenuController, dish_controller: DishController, faker: Faker
) -> None:
    # Prepare
    menu_create = MenuCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        price=random.uniform(2.99, 99.99),
        discount=random.randint(0, 100),
    )
    created_menu = await menu_controller.create_menu(menu_create)

    dish_create = DishCreate(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        category=random.choice(list(Category)),
        ingredients=faker.text(max_nb_chars=24),
        price=random.uniform(0.99, 99.99),
        halal=random.choice([True, False]),
    )
    created_dish = await dish_controller.create_dish(dish_create)

    menu_dish_links_create = MenuDishLinksCreate(
        dish_ids=[created_dish.id], menu_id=created_menu.id
    )
    await menu_controller.add_dish_to_menu(
        menu_id=created_menu.id, menu_dish_links_create=menu_dish_links_create
    )

    # Act
    await menu_controller.delete_dish_from_menu(
        menu_id=created_menu.id, dish_id=created_dish.id
    )

    # Assert
    updated_menu = await menu_controller.get_menu_by_id(created_menu.id)
    assert created_dish.id not in [dish.id for dish in updated_menu.dishes]


@pytest.mark.asyncio
async def test_delete_dish_from_menu_not_found_error(
    menu_controller: MenuController, faker: Faker
) -> None:
    # Prepare
    nonexistent_menu_id = faker.uuid4()
    nonexistent_dish_id = faker.uuid4()

    # Act & Assert
    with pytest.raises(DishInMenuNotFoundError):
        await menu_controller.delete_dish_from_menu(
            menu_id=nonexistent_menu_id, dish_id=nonexistent_dish_id
        )


@pytest.mark.asyncio
async def test_get_discounted_menus(
    menu_controller: MenuController, faker: Faker
) -> None:
    # Prepare
    for _ in range(5):
        menu_create = MenuCreate(
            title=faker.text(max_nb_chars=12),
            description=faker.text(max_nb_chars=24),
            price=random.uniform(2.99, 99.99),
            discount=random.uniform(0.01, 100),
        )
        await menu_controller.create_menu(menu_create)

    for _ in range(3):
        menu_create = MenuCreate(
            title=faker.text(max_nb_chars=12),
            description=faker.text(max_nb_chars=24),
            price=random.uniform(2.99, 99.99),
            discount=0,  # No discount
        )
        await menu_controller.create_menu(menu_create)

    # Act
    all_discounted_menus = await menu_controller.get_discounted_menus()

    # Assert
    assert len(all_discounted_menus) == 5
    for menu in all_discounted_menus:
        assert menu.discount > 0
