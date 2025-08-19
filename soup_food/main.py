from fastapi import FastAPI, Request, Depends
from dependency_injector.wiring import inject, Provide

from soup_food.models.food import Food, FoodCreate
from soup_food.container import Container
from soup_food.repository.repository import Repository


container = Container()
container.config.repo_type.from_env("REPO_TYPE", default="production")
container.wire(modules=[__name__])


app = FastAPI(root_path="/api")
app.container = container


@app.get("/", response_model=dict)
@inject
async def read_root(
    request: Request, repository: Repository = Depends(Provide[Container.repo])
):
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
@inject
async def get_all_foods_endpoint(
    repository: Repository = Depends(Provide[Container.repo]),
):
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
