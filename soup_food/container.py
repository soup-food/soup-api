from dependency_injector import containers, providers
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from soup_food.repository.mongo_db_repository import MongoDBRepository
from soup_food.repository.in_memory_repository import InMemoryRepository


def get_collection(
    client: AsyncIOMotorClient,
    db_name: str,
    collection_name: str,
) -> AsyncIOMotorCollection:
    return client[db_name][collection_name]


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Mongo client singleton
    mongo_client = providers.Singleton(
        AsyncIOMotorClient,
        config.mongo.connection_string,
        serverSelectionTimeoutMS=config.mongo.timeout,
    )

    mongo_collection = providers.Singleton(
        get_collection,
        client=mongo_client,
        db_name=config.mongo.database,
        collection_name=config.mongo.collection,
    )

    # Selector to pick repository implementation
    repo_selector = providers.Selector(
        config.repo_type,
        mongo=providers.Factory(MongoDBRepository, collection=mongo_collection),
        inmemory=providers.Factory(InMemoryRepository),
    )

    # Factory that resolves the selected repository
    repo = repo_selector
