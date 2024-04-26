from uuid import UUID

from pydantic_extra_types.phone_numbers import PhoneNumber


class BaseError(Exception):
    def __init__(self, name: str, message: str, status_code: int):
        self.name = name
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DishNotFoundError(BaseError):
    def __init__(
        self, dish_id: UUID, status_code: int = 404, name: str = "DishNotFoundError"
    ):
        self.name = name
        self.message = f"Dish with ID {dish_id} not found"
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )


class DishAlreadyExistsError(BaseError):
    def __init__(
        self, title: str, status_code: int = 409, name: str = "DishAlreadyExistsError"
    ):
        self.name = name
        self.message = f"Dish with title: {title} already exists"
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )


class MenuNotFoundError(BaseError):
    def __init__(
        self, menu_id: UUID, status_code: int = 404, name: str = "MenuNotFoundError"
    ):
        self.name = name
        self.message = f"Menu with ID {menu_id} not found"
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )


class MenuAlreadyExistsError(BaseError):
    def __init__(
        self, title: str, status_code: int = 409, name: str = "MenuAlreadyExistsError"
    ):
        self.name = name
        self.message = f"Menu with title: {title} already exists"
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )


class ReservationNotFoundError(BaseError):
    def __init__(
        self,
        reservation_id: UUID,
        status_code: int = 404,
        name: str = "ReservationNotFoundError",
    ):
        self.name = name
        self.message = f"Reservation with ID {reservation_id} not found"
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )


class MenuDishLinksNotFoundError(BaseError):
    def __init__(
        self, menu_id: UUID, status_code: int = 404, name: str = "MenuNotFoundError"
    ):
        self.name = name
        self.message = f"Menu with ID {menu_id} not found"
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )
