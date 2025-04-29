import typing


class ApplicationException(Exception):
    _MESSAGE: typing.ClassVar[str] = 'Internal Server Error'

    def __init__(self, message: str | None = None, extra: dict | None = None) -> None:
        if message is None:
            message = self._MESSAGE

        if extra is None:
            extra = {}

        self.message = message
        self.extra = extra
