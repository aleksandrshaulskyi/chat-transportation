from domain.exceptions.base import BaseException


class ApplicationException(BaseException):
    """
    An exception risen should something go wrong on the application layer.
    All application layer exceptions inherit from this exception.
    """
