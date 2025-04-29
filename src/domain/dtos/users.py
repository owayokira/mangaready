from pydantic import BaseModel, EmailStr


class CreateUserDTO(BaseModel):
    email: EmailStr
    username: str
    password: str
    password_salt: str
