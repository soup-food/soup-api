import os
from typing import Optional, override, Mapping
from uuid import UUID

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo.errors import PyMongoError

from sus_food.models.food import Food, FoodUpdate, FoodCreate
from sus_food.repository.repository import Repository

load_dotenv()

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING") 
MONGO_DATABASE = os.getenv("MONGO_DATABASE")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
CONNECTION_TIMEOUT = int(os.getenv("CONNECTION_TIMEOUT", 2000))

class MongoDBRepository(Repository):
    def __init__(self):
        self._collection: AsyncIOMotorCollection = AsyncIOMotorClient(
            MONGO_CONNECTION_STRING,
            serverSelectionTimeoutMS=CONNECTION_TIMEOUT
        )[MONGO_DATABASE][MONGO_COLLECTION]

    @staticmethod
    def _map_doc_to_food(doc: Mapping) -> Optional[Food]:
        """Helper to map a MongoDB document to a Pydantic Food model."""
        if doc:
            return Food(**doc)
        return None

    @override
    async def ping(self) -> bool:
        """
        Check if the MongoDB connection is alive.
        Returns True if the connection is successful, False otherwise.
        """
        try:
            await self._collection.database.client.server_info()
            return True
        except PyMongoError:
            return False

    @override
    async def get_food_by_id(self, food_id: UUID) -> Optional[Food]:
        try:
            doc = await self._collection.find_one({"_id": str(food_id)})
            if doc:
                return self._map_doc_to_food(doc)
        except PyMongoError as e:
            # TODO: Handle logging
            return None

    @override
    async def get_all_foods(self) -> list[Food]:
        foods = []
        try:
            cursor = self._collection.find({})
            docs = await cursor.to_list(length=None)
            for doc in docs:
                foods.append(self._map_doc_to_food(doc))
            return foods
        except PyMongoError as e:
            #TODO: Handle logging
            return []

    @override
    async def add_food(self, food_create: FoodCreate) -> Optional[UUID]:
        try:
            new_food = Food(**food_create.model_dump())
            food_data = new_food.model_dump(by_alias=True)
            food_data["_id"] = str(new_food.id) # Ensure _id is a string for storage

            result = await self._collection.insert_one(food_data)
            if result.inserted_id:
                return new_food.id
            return None
        except PyMongoError as e:
            # TODO: Handle logging
            return None

    @override
    async def update_food(self, food_update: FoodUpdate) -> bool:
        try:
            food_id_to_update = food_update.id

            update_data = food_update.model_dump(exclude_unset=True,
                                                 by_alias=True)

            update_data.pop("_id", None)

            if not update_data:
                print(f"No update data provided for food ID: {food_id_to_update}")
                return False

            result = await self.collection.update_one(
                {"_id": str(food_id_to_update)},
                {"$set": update_data}
            )

            return result.modified_count > 0
        except PyMongoError as e:
            # TODO: Handle logging
            return False

    @override
    async def delete_food(self, food_id: UUID) -> bool:
        try:
            result = await self._collection.delete_one({"_id": str(food_id)})
            return result.deleted_count > 0
        except PyMongoError as e:
            # TODO: Handle logging
            return False

