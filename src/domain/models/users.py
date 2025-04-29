import datetime
import uuid


class UserStorage:
    id: uuid.UUID
    email: str
    username: str
    password: str
    password_salt: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
