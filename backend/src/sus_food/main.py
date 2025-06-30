from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()


client = AsyncIOMotorClient(MONGODB_CONNECTION_STRING, uuidRepresentation="standard")
db = client.todolist
todos = db.todos

@app.get("/hello")
def read_root():
    return {"message": "Hello Madda!!"}

@app.get("/likes")
def read_likes():
    return