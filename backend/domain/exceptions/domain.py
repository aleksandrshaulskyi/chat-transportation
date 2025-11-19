from domain.exceptions import BaseException


class DomainException(BaseException):
    """
    An exception risen should something go wrong on the domain layer.
    All domain layer exceptions inherit from this exception.
    """
