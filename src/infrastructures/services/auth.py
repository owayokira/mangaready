import hashlib

from src.domain import interfaces


class SHA256PasswordHasher(interfaces.PasswordHasherProtocol):
    def __init__(self, pepper: str, count: int) -> None:
        self._pepper = pepper
        self._count = count

    def hash(self, password: str, salt: str) -> str:
        for _ in range(self._count):
            password = hashlib.sha256((password + salt + self._pepper).encode("utf-8")).hexdigest()

        return password

    def check(self, password: str, salt: str, hashed_password: str) -> bool:
        return self.hash(password, salt) == hashed_password
