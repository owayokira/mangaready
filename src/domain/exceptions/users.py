from . import ApplicationException


class EmailAlreadyExistsException(ApplicationException):
    _MESSAGE = "Email already exists"


class UsernameAlreadyExistsException(ApplicationException):
    _MESSAGE = "Username already exists"


class UserNotFoundException(ApplicationException):
    _MESSAGE = "User not found"
