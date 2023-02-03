from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from config.db import collection_name
from datetime import datetime
from models.user import UserModel, UpdateUserModel
from schemas.users_schemas import user_serializer, users_serializer

user_register_api_router = APIRouter()


@user_register_api_router.get("/users")
async def get_all_user():
    users = users_serializer(collection_name.find())
    return JSONResponse(status_code=200, content=users)


@user_register_api_router.get("/users/{user_id}", response_description="Get a single user", response_model=UserModel)
async def show_student(user_id: str):
    # add await
    if (user := collection_name.find_one({"_id": user_id})) is not None:
        return user
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@user_register_api_router.post("/users", response_description="Add new User", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = collection_name.insert_one(user)
    created_user = collection_name.find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@user_register_api_router.put("/users/{user_id}", response_description="Update a user", response_model=UserModel)
async def update_user(user_id: str, user: UpdateUserModel = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        update_result = collection_name.update_one(
            {"_id": user_id}, {"$set": user})  # add await

        if update_result.modified_count == 1:
            if (
                # add await
                updated_user := collection_name.find_one({"_id": user_id})
            ) is not None:
                return JSONResponse(status_code=202, content=updated_user)

    # add await
    if (existing_user := collection_name.find_one({"_id": user_id})) is not None:
        return JSONResponse(status_code=202, content=existing_user)

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@user_register_api_router.delete("/users/{user_id}", response_description="Delete a user")
async def delete_user(user_id: str):
    delete_result = collection_name.delete_one({"_id": user_id})  # add await

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=202, content=f"User with {user_id} was deleted")

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")
