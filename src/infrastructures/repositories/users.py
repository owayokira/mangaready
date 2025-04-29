import uuid

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain import dtos, exceptions, interfaces, models


class SQLAlchemyUserRepository(interfaces.UserRepositoryProtocol):
    _EMAIL_ALREADY_EXISTS_ERROR_MESSAGE = (
        'duplicate key value violates unique constraint "user_email_key"')
    _USERNAME_ALREADY_EXISTS_ERROR_MESSAGE = (
        'duplicate key value violates unique constraint "user_username_key"')

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, dto: dtos.CreateUserDTO) -> uuid.UUID:
        user_id = uuid.uuid4()
        stmt = sa.insert(models.UserStorage).values(id=user_id, **dto.model_dump())

        try:
            await self._session.execute(stmt)
        except sa.exc.IntegrityError as exc:
            orig = str(exc.orig)

            if self._EMAIL_ALREADY_EXISTS_ERROR_MESSAGE in orig:
                raise exceptions.EmailAlreadyExistsException(extra={"username": dto.username}) from exc

            if self._USERNAME_ALREADY_EXISTS_ERROR_MESSAGE in orig:
                raise exceptions.UsernameAlreadyExistsException(extra={"username": dto.username}) from exc

            raise exceptions.ApplicationException from exc

        return user_id
