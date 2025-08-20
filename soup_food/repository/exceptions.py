class RepositoryError(Exception):
    """Base class for repository errors."""

    pass


class FoodNotFoundError(RepositoryError):
    """Raised when a food item is not found."""

    def __init__(self, food_id):
        super().__init__(f"Food with id {food_id} not found")
        self.food_id = food_id
