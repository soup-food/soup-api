from fastapi import FastAPI

from sus_food.models.food import Food, FoodCreate
from sus_food.repository.repository_factory import RepositoryFactory

app = FastAPI()

repository = RepositoryFactory.create_repository()


@app.get("/")
async def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return "Connection alive" if await repository.ping() else "Connection not alive"


@app.get("/get_all_foods", response_model=list[Food])
async def get_all_foods() -> list[Food]:
    """
    Endpoint to retrieve all food items.
    """
    await repository.add_food(FoodCreate(
        name="Passatelli in brodo",
        calories=400,
        description="Pasta a base di pane grattugiato, parmigiano e uova, servita in brodo di carne. Comfort food romagnolo per eccellenza."
    ))
    response = await repository.get_all_foods()
    print(response)
    return response
