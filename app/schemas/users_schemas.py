def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "last_name": user["last_name"],
        "document_type": user["document_type"],
        "document_number": user["document_number"],
        "gender": user["gender"],
        "hashed_password": user["hashed_password"],
        "age": user["age"],
        "email": user["email"],
        "kyc": user['kyc'],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]
