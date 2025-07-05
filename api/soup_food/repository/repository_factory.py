from soup_food.repository.mongo_db_repository import MongoDBRepository
from soup_food.repository.repository import Repository


class RepositoryFactory:
    """
    Factory class to create repository instances.
    """

    @staticmethod
    def create_repository() -> Repository:
        """
        Creates an instance of a Repository implementation.

        Returns:
            Repository: An instance of a Repository implementation,
                        currently MongoDBRepository.

        Usage:
            >>> repo = RepositoryFactory.create_repository()
        """
        return MongoDBRepository()
