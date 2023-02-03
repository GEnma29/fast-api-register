def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "lastName": user["lastName"],
        "gender": user["gender"],
        "age": user["age"],
        "email": user["email"],
        "kyc": user['kyc'],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]
