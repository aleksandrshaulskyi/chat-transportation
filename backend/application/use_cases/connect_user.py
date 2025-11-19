from application.ports import RabbitMQManagerPort, WebSocketHubPort
from application.protocols import WebSocket


class ConnectUserUseCase:
    """
    The use case that orchestrates the connection process of a user.
    """

    def __init__(
        self,
        user_id: int,
        websocket: WebSocket,
        websocket_hub: WebSocketHubPort,
        rabbitmq_manager: RabbitMQManagerPort,
    ) -> None:
        """
        Initialize the use case.

        Args:
            user_id (int): The id of a user that needs to be connected.
            websocket (WebSocket): The protocol for WebSocket.
            websocket_hub (WebSocketHubPort): The port for websocket hub.
            rabbitmq_manager (RabbitMQManagerPort): The port for RabbitMQ.
        """
        self.user_id = user_id
        self.websocket = websocket
        self.websocket_hub = websocket_hub
        self.rabbitmq_manager = rabbitmq_manager

    async def execute(self) -> None:
        """
        Connect the user to websocket hub and start consumption process from RabbitMQ.
        """
        await self.connect_user()
        await self.start_consuming()

    async def connect_user(self) -> None:
        """
        Connect the user to the websocket hub.
        """
        await self.websocket_hub.connect_user(user_id=self.user_id, websocket=self.websocket)

    async def start_consuming(self) -> None:
        """
        Create the task for consumption from RabbitMQ ephemeral queue.
        """
        await self.rabbitmq_manager.start_consumption_process(user_id=self.user_id)
