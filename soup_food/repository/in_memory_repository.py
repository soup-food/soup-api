from typing import Optional, override, List
from uuid import UUID

from soup_food.models.food import Food, FoodCreate, FoodUpdate
from soup_food.repository.repository import Repository


class InMemoryRepository(Repository):
    def __init__(self):
        self._foods: List[Food] = []

    @override
    async def ping(self) -> bool:
        return True

    @override
    async def get_food_by_id(self, food_id: UUID) -> Optional[Food]:
        return next((food for food in self._foods if food.id == food_id), None)

    @override
    async def get_all_foods(self) -> list[Food]:
        return self._foods

    @override
    async def add_food(self, food_create: FoodCreate) -> UUID:
        new_food = Food(**food_create.model_dump())
        self._foods.append(new_food)
        return new_food.id

    @override
    async def update_food(self, food_update: FoodUpdate) -> bool:
        for i, food in enumerate(self._foods):
            if food.id == food_update.id:
                update_data = food_update.model_dump(exclude_unset=True)
                updated_food = food.model_copy(update=update_data)
                self._foods[i] = updated_food
                return True
        return False

    @override
    async def delete_food(self, food_id: UUID) -> bool:
        initial_length = len(self._foods)
        self._foods = [food for food in self._foods if food.id != food_id]
        return len(self._foods) < initial_length
