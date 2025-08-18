from fastapi import FastAPI, Request

from soup_food.models.food import Food, FoodCreate
from soup_food.container import Container

app = FastAPI(root_path="/api")

container = Container()
container.config.repo_type.override("inmemory")  # or "mongo"

repository = container.repo()  # Get the repository instance


@app.get("/", response_model=dict)
async def read_root(request: Request):
    """
    Root endpoint to check if the API is running.
    Returns the full request URL and connection status.
    """
    connection_alive = await repository.ping()
    return {
        "url": str(request.url),
        "status": "Connection alive" if connection_alive else "Connection not alive",
    }


@app.get("/get_all_foods", response_model=list[Food])
async def get_all_foods_endpoint():
    """
    Endpoint to retrieve all food items.
    Adds a sample food before fetching all.
    """
    await repository.add_food(
        FoodCreate(
            name="Passatelli in brodo",
            calories=400,
            description=(
                "Pasta a base di pane grattugiato, parmigiano e uova, "
                "servita in brodo di carne. Comfort food romagnolo per eccellenza."
            ),
        )
    )
    foods = await repository.get_all_foods()
    return foods
