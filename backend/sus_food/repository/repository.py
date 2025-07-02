from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from sus_food.models.food import FoodCreate, Food, FoodUpdate


class Repository(ABC):
    """
    Abstract base class for food repository.
    This class defines the interface for interacting with food items in a database.
    """

    @abstractmethod
    async def ping(self) -> bool:
        pass

    @abstractmethod
    async def get_food_by_id(self, food_id: UUID) -> Optional[Food]:
        pass

    @abstractmethod
    async def get_all_foods(self) -> list[Food]:
        pass

    @abstractmethod
    async def add_food(self, food_create: FoodCreate) -> UUID:
        pass

    @abstractmethod
    async def update_food(self, food_update: FoodUpdate) -> bool:
        pass

    @abstractmethod
    async def delete_food(self, food_id: UUID) -> bool:
        pass
