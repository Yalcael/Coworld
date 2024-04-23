from uuid import UUID


class BaseError(Exception):
    def __init__(self, name: str, message: str, status_code: int):
        self.name = name
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DishNotFoundError(BaseError):
    def __init__(self, dish_id: UUID, status_code: int = 404, name: str = "DishNotFoundError"):
        self.name = name
        self.message = f"Dish with ID {dish_id} not found"
        self.status_code = status_code
        super().__init__(name=self.name, message=self.message, status_code=self.status_code)


class DishAlreadyExistsError(BaseError):
    def __init__(self, title: str, status_code: int = 409, name: str = "DishAlreadyExistsError"):
        self.name = name
        self.message = f"Dish with title: {title} already exists"
        self.status_code = status_code
        super().__init__(name=self.name, message=self.message, status_code=self.status_code)
