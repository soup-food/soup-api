from abc import ABC, abstractmethod
from typing import Optional, Sequence
from uuid import UUID

from soup_food.models.food import FoodCreate, Food, FoodUpdate


class Repository(ABC):
    """Abstract base class for food repository."""

    @abstractmethod
    async def ping(self) -> bool:
        """Check if the repository is reachable."""
        pass

    @abstractmethod
    async def get_food_by_id(self, food_id: UUID) -> Optional[Food]:
        """Retrieve a food item by its UUID."""
        pass

    @abstractmethod
    async def get_all_foods(
        self, *, name_contains: Optional[str] = None
    ) -> Sequence[Food]:
        """Return all foods, optionally filtering by name."""
        pass

    @abstractmethod
    async def add_food(self, food_create: FoodCreate) -> Food:
        """Add a new food item and return it (with assigned ID)."""
        pass

    @abstractmethod
    async def update_food(self, food_update: FoodUpdate) -> None:
        """Update a food item. Raise if not found."""
        pass

    @abstractmethod
    async def delete_food(self, food_id: UUID) -> None:
        """Delete a food item. Raise if not found."""
        pass
