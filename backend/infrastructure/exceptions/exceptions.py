from domain.exceptions import BaseException


class AuthenticationException(BaseException):
    """
    The exception to be raisen if something goes wrong while authentication process.
    """
    ...
