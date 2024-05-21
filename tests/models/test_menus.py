import pytest
import random
from faker import Faker
from coworld.models.menus import MenuBase


@pytest.mark.asyncio
async def test_create_menu_base_when_discount_is_0(
    faker: Faker
) -> None:
    # Prepare / Act
    menu_base = MenuBase(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        price=random.uniform(2.99, 99.99),
        discount=0,
    )

    # Assert
    assert menu_base.discounted_price == menu_base.price


@pytest.mark.asyncio
async def test_create_menu_base_when_discount_is_superior_than_0(
    faker: Faker
) -> None:
    # Prepare / Act
    menu_base = MenuBase(
        title=faker.text(max_nb_chars=12),
        description=faker.text(max_nb_chars=24),
        price=50,
        discount=10,
    )

    # Assert
    assert menu_base.discounted_price == 45
