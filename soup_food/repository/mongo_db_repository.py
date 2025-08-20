from typing import Optional, override, Mapping, Sequence
from uuid import UUID
from pymongo.errors import PyMongoError

from soup_food.models.food import Food, FoodUpdate, FoodCreate
from soup_food.repository.repository import Repository
from soup_food.repository.exceptions import RepositoryError, FoodNotFoundError


class MongoDBRepository(Repository):
    def __init__(self, collection):
        self._collection = collection

    @staticmethod
    def _map_doc_to_food(doc: Mapping) -> Optional[Food]:
        return Food(**doc) if doc else None

    @override
    async def ping(self) -> bool:
        try:
            await self._collection.database.client.server_info()
            return True
        except PyMongoError:
            return False

    @override
    async def get_food_by_id(self, food_id: UUID) -> Optional[Food]:
        try:
            doc = await self._collection.find_one({"_id": str(food_id)})
            return self._map_doc_to_food(doc)
        except PyMongoError as e:
            raise RepositoryError(f"Database error: {e}")

    @override
    async def get_all_foods(
        self, *, name_contains: Optional[str] = None
    ) -> Sequence[Food]:
        query = {}
        if name_contains:
            query["name"] = {"$regex": name_contains, "$options": "i"}
        try:
            cursor = self._collection.find(query)
            docs = await cursor.to_list(length=None)
            return [self._map_doc_to_food(doc) for doc in docs if doc]
        except PyMongoError as e:
            raise RepositoryError(f"Database error: {e}")

    @override
    async def add_food(self, food_create: FoodCreate) -> Food:
        try:
            new_food = Food(**food_create.model_dump())
            food_data = new_food.model_dump(by_alias=True)
            food_data["_id"] = str(new_food.id)
            result = await self._collection.insert_one(food_data)
            if result.inserted_id:
                return new_food
            raise RepositoryError("Failed to insert food")
        except PyMongoError as e:
            raise RepositoryError(f"Database error: {e}")

    @override
    async def update_food(self, food_update: FoodUpdate) -> None:
        try:
            update_data = food_update.model_dump(exclude_unset=True, by_alias=True)
            update_data.pop("_id", None)
            if not update_data:
                raise RepositoryError("No update data provided")

            result = await self._collection.update_one(
                {"_id": str(food_update.id)}, {"$set": update_data}
            )
            if result.modified_count == 0:
                raise FoodNotFoundError(food_update.id)
        except PyMongoError as e:
            raise RepositoryError(f"Database error: {e}")

    @override
    async def delete_food(self, food_id: UUID) -> None:
        try:
            result = await self._collection.delete_one({"_id": str(food_id)})
            if result.deleted_count == 0:
                raise FoodNotFoundError(food_id)
        except PyMongoError as e:
            raise RepositoryError(f"Database error: {e}")
