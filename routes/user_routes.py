from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from config.db import collection_name
from models.user import UserModel
from schemas.users_schemas import user_serializer, users_serializer

user_register_api_router = APIRouter()


@user_register_api_router.get("/users")
async def get_all_user():
    users = users_serializer(collection_name.find())
    return JSONResponse(status_code=200, content=users)


@user_register_api_router.get("/users/{user_id}", response_description="Get a single user", response_model=UserModel)
async def show_student(user_id: str):
    if (user := collection_name.find_one({"_id": user_id})) is not None:
        return user
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@user_register_api_router.post("/users", response_description="Add new User", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = collection_name.insert_one(user)
    created_user = collection_name.find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)
