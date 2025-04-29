import typing
import uuid

from src.domain import dtos


class UserRepositoryProtocol(typing.Protocol):
    async def create(self, dto: dtos.CreateUserDTO) -> uuid.UUID:
        ...
