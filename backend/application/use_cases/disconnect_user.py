from application.ports import RedisManagerPort, WebSocketHubPort
from application.protocols import WebSocket


class DisconnectUserUseCase:
    """
    The use case that orchestrates the user disconnect process.
    """

    def __init__(
        self,
        user_id: int,
        websocket: WebSocket,
        websocket_hub: WebSocketHubPort,
        redis_manager: RedisManagerPort,
    ) -> None:
        """
        Initialize the use case.

        Args:
            user_id (int): The id of a user that needs to be connected.
            websocket (WebSocket): The protocol for WebSocket.
            websocket_hub (WebSocketHubPort): The port for websocket hub.
            redis_manager (RedisManagerPort): The port for redis manager.
        """
        self.user_id = user_id
        self.websocket = websocket
        self.websocket_hub = websocket_hub
        self.redis_manager = redis_manager

    async def execute(self) -> None:
        """
        Disconnect the user from websocket hub and unmap connection from Redis.
        """
        await self.disconnect_user()
        await self.remove_mapping()

    async def disconnect_user(self) -> None:
        """
        Disconnect the user from the websocket hub.
        """
        await self.websocket_hub.disconnect_user(user_id=self.user_id, websocket=self.websocket)

    async def remove_mapping(self) -> None:
        """
        Remove the connection from Redis.
        """
        await self.redis_manager.remove_mapping(user_id=self.user_id)
