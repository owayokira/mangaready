import uuid

from src.domain import dtos, interfaces


class RegisterUserUsecase:
    def __init__(
        self,
        uow: interfaces.UnitOfWorkProtocol,
        password_hasher: interfaces.PasswordHasherProtocol,
    ) -> None:
        self._uow = uow
        self._password_hasher = password_hasher

    async def execute(self, dto: dtos.RegisterUserDTO) -> dtos.RegisteredUserDTO:
        async with self._uow.begin():
            password_salt = uuid.uuid4().hex
            user_id = await self._uow.user.create(dtos.CreateUserDTO(
                email=dto.email,
                username=dto.username,
                password=self._password_hasher.hash(dto.password, password_salt),
                password_salt=password_salt,
            ))

        return dtos.RegisteredUserDTO(id=user_id)
