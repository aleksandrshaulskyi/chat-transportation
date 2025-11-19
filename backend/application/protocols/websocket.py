from typing import Protocol


class WebSocket(Protocol):
    """
    A protocol that defines the abstraction for a WebSocket connection.

    This protocol can be used for type-checking in layers that should not depend
    directly on the framework (e.g. FastAPI or Starlette) implementation.

    Any object is considered compatible.
    """
    ...
