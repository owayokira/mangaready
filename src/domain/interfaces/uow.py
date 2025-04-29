import typing

from .users import UserRepositoryProtocol


class UnitOfWorkProtocol(typing.Protocol):
    user: UserRepositoryProtocol

    def begin(self) -> typing.AsyncContextManager:
        ...

    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...
