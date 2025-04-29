import uuid

from pydantic import BaseModel, EmailStr


class RegisterUserDTO(BaseModel):
    email: EmailStr
    username: str
    password: str


class RegisteredUserDTO(BaseModel):
    id: uuid.UUID
