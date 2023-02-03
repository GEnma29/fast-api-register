from pymongo import MongoClient
from typing import TypedDict
from config.env import settings
from pymongo.database import Database
from models.user import UserModel

client: MongoClient = MongoClient(
    f'mongodb+srv://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@cluster0.vryyi0e.mongodb.net/?retryWrites=true&w=majority')

db: Database = client.todo_pago

collection_name = db[settings.MONGO_COLLETION_USER]
