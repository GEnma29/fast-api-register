def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "lastName": user["lastName"],
        "gender": user["gender"],
        "age": user["age"],
        "email": user["email"],
        "kyc": user['kyc']
    }


def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]
