from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from app.config.db import collection_name
from typing import List
from app.models.user import UserModel, UpdateUserModel
from app.schemas.users_schemas import user_serializer, users_serializer
from app.utilities.encrypt import get_password_hash


user_register_api_router = APIRouter()


@user_register_api_router.get("/users",  response_description="Get all  users", response_model=List[UserModel])
async def get_all_user():
    users = users_serializer(collection_name.find())
    return JSONResponse(status_code=200, content=users)


@user_register_api_router.get("/users/{user_id}", response_description="Get a single user", response_model=UserModel)
async def show_student(user_id: str):
    if (user := collection_name.find_one({"_id": user_id})) is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User {user_id} not found")


@user_register_api_router.post("/users", response_description="Add new User", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    user.hashed_password = get_password_hash(user.hashed_password)
    user = jsonable_encoder(user)
    new_user = collection_name.insert_one(user)
    created_user = collection_name.find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@user_register_api_router.put("/users/{user_id}", response_description="Update a user", response_model=UserModel)
async def update_user(user_id: str, user: UpdateUserModel = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        update_result = collection_name.update_one(
            {"_id": user_id}, {"$set": user})

        if update_result.modified_count == 1:
            if (
                updated_user := collection_name.find_one({"_id": user_id})
            ) is not None:
                return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=updated_user)

    if (existing_user := collection_name.find_one({"_id": user_id})) is not None:
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=existing_user)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User {user_id} not found")
1


@user_register_api_router.delete("/users/{user_id}", response_description="Delete a user")
async def delete_user(user_id: str):
    delete_result = collection_name.delete_one({"_id": user_id})  # add await

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=f"User with {user_id} was deleted")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User {user_id} not found")
