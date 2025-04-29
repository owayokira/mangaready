import typing


class PasswordHasherProtocol(typing.Protocol):
    def hash(self, password: str, salt: str) -> str:
        ...

    def check(self, password: str, salt: str, hashed_password: str) -> bool:
        ...
