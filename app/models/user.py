from typing import List, Optional
from bson import ObjectId
from passlib.context import CryptContext
from pydantic import BaseModel, Field, EmailStr, root_validator
from datetime import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    last_name: str = Field(...)
    document_type: str = Field(...)
    document_number: str = Field(...)
    gender: str = Field(...)
    hashed_password: str = Field(...)
    age: int = Field(...)
    email: EmailStr = Field(...)
    kyc: bool = Field(...)
    created_at: datetime = datetime.utcnow().isoformat()
    updated_at: datetime = datetime.utcnow().isoformat()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane",
                "last_name": "Doe",
                "document"
                "gender": "Male",
                "age": "25",
                "email": "jdoe@example.com",
                "kyc": False,
            }
        }


class UpdateUserModel(BaseModel):
    name: Optional[str]
    last_name: Optional[str]
    document_type: Optional[str]
    document_number: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    email: Optional[EmailStr]
    kyc: Optional[bool]

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane",
                "lastName": "Doe",
                "gender": "Male",
                "age": "25",
                "email": "jdoe@example.com",
                "kyc": False,
            }
        }

    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.utcnow().isoformat()
        return values
