import typing

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain import interfaces


class SQLAlchemyUnitOfWork(interfaces.UnitOfWorkProtocol):
    def __init__(
        self,
        user_repository: interfaces.UserRepositoryProtocol,
        session: AsyncSession,
    ) -> None:
        self.user = user_repository
        self._session = session

    def begin(self) -> typing.AsyncContextManager:
        return self._session.begin()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
