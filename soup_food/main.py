from fastapi import FastAPI, Request

from soup_food.models.food import Food, FoodCreate
from soup_food.repository.repository_factory import RepositoryFactory

repository = RepositoryFactory.create_repository()

app = FastAPI(root_path="/api")


@app.get("/", response_model=dict)
async def read_root(request: Request):
    """
    Root endpoint to check if the API is running.
    Returns the full request URL and connection status.
    """
    return {
        "url": str(request.url),
        "status": "Connection alive" if await repository.ping() else "Connection not alive"
    }



@app.get("/hello")
async def get_all_foods():
    return "Hello"


@app.get("/get_all_foods", response_model=list[Food])
async def get_all_foods() -> list[Food]:
    """
    Endpoint to retrieve all food items.
    """
    await repository.add_food(
        FoodCreate(
            name="Passatelli in brodo",
            calories=400,
            description="Pasta a base di pane grattugiato, parmigiano e uova, servita in brodo di carne. Comfort food romagnolo per eccellenza.",
        )
    )
    response = await repository.get_all_foods()
    print(response)
    return response
