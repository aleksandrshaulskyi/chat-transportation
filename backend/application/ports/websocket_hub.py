from abc import ABC, abstractmethod

from application.protocols import WebSocket


class WebSocketHubPort(ABC):
    """
    The port for the websocket hub that orchestrates the websocket connections.

    This abstraction only implements the method to map a user connection.
    """

    @abstractmethod
    async def connect_user(self, user_id: int, websocket: WebSocket) -> None:
        """
        This method is responsible for adding a user connection to the map of
        hub connections that is later used for message routing.

        Technically adds a key-value pair to the dictionary that allows to get the
        websocket by user_id.
        """
        ...

    @abstractmethod
    async def disconnect_user(self, user_id: int, websocket: WebSocket) -> None:
        """
        This method is responsible for disconnecting a user from the websocket shard.
        """
        ...
