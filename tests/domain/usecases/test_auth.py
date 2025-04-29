import uuid

from pytest_mock import MockerFixture

from src.domain import dtos, usecases
from tests.helpers import DATA_DIR, load_json_fixture


class TestRegisterUserUsecase:
    _CASE_DIR = DATA_DIR / "domain" / "usecases" / "auth"

    async def test_register_user_usecase(self, mocker: MockerFixture) -> None:
        case = self._CASE_DIR / "register_user"

        uow = mocker.Mock()
        uow.begin = mocker.MagicMock()

        password_hasher = mocker.Mock()
        password_hasher.hash = mocker.MagicMock(return_value="something")

        user_id = uuid.uuid4()
        uow.user.create = mocker.AsyncMock(return_value=user_id)

        usecase = usecases.RegisterUserUsecase(uow, password_hasher)
        dto = dtos.RegisterUserDTO(**load_json_fixture(case / "dto"))

        assert await usecase.execute(dto) == dtos.RegisteredUserDTO(id=user_id)
