from fastapi import FastAPI, Request, Depends, HTTPException
from typing import List

from soup_food.models.food import Food, FoodCreate
from soup_food.container import Container
from soup_food.repository.repository import Repository
from soup_food.repository.exceptions import RepositoryError

container = Container()
container.config.repo_type.from_env("REPO_TYPE", default="inmemory")

if container.config.repo_type() == "mongo":
    container.config.mongo.connection_string.from_env("MONGO_CONNECTION_STRING")
    container.config.mongo.database.from_env("MONGO_DATABASE")
    container.config.mongo.collection.from_env("MONGO_COLLECTION")
    container.config.mongo.timeout.from_env("CONNECTION_TIMEOUT", as_=int)

app = FastAPI(root_path="/api")
app.container = container


def get_repository(request: Request) -> Repository:
    return request.app.container.repo()


@app.get("/", response_model=dict)
async def read_root(request: Request, repository: Repository = Depends(get_repository)):
    try:
        alive = await repository.ping()
        return {
            "message": "Welcome to the Soup Food API!",
            "repository_type": type(repository).__name__,
            "status": "Connection alive" if alive else "Connection not alive",
        }
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add_sample_food")
async def add_sample_food_endpoint(
    repository: Repository = Depends(get_repository),
):
    try:
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
        return {"message": "Sample food added."}
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_all_foods", response_model=List[Food])  # use typing.List
async def get_all_foods_endpoint(
    repository: Repository = Depends(get_repository),
):
    try:
        return await repository.get_all_foods()
    except RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e))
