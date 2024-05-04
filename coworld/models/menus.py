from pydantic import PositiveFloat, computed_field
from sqlmodel import Field, SQLModel


class MenuBase(SQLModel):
    title: str = Field(unique=True, index=True)
    description: str
    price: PositiveFloat
    discount: float = Field(default=0.0)

    @computed_field
    def discounted_price(self) -> float:
        if self.discount > 0.0:
            discounted_price = self.price * (1 - self.discount / 100)
            return round(discounted_price, 2)
        return self.price


class MenuCreate(MenuBase):
    pass


class MenuUpdate(SQLModel):
    price: PositiveFloat | None = None
    title: str | None = None
    description: str | None = None
    discount_percentage: float | None = None
