from coworld.controllers.menus import MenuController
import pytest
import random
from faker import Faker
from sqlmodel import Session, select

from coworld.models.errors import MenuAlreadyExistsError
from coworld.models.menus import MenuCreate
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
async def test_menu_already_exist_error(
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
