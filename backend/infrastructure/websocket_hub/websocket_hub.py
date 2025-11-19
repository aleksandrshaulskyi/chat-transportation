from json import JSONDecodeError

from fastapi import WebSocket

from application.ports import WebSocketHubPort


class WebSocketHub(WebSocketHubPort):
    """
    The hub that is responsible for the orchestrating the websockets workflow.
    """

    def __init__(self) -> None:
        """
        Initializes the hub.
        """
        self.connections = {}

    async def connect_user(self, user_id: int, websocket: WebSocket) -> None:
        """
        Connect a user to the hub.

        Accept the websocket connection.
        Store the connection mapping.

        Args:
            user_id (int): An id of a user that is trying to connect to the websocket endpoint.
            websocket (WebSocket): An instance of FastAPI WebSocket.
        """
        await websocket.accept()
        self.connections.update({user_id: websocket})

    async def receive(self, websocket: WebSocket) -> dict | None:
        """
        Receive a single message from the websocket channel and check whether a valid JSON was sent.

        Args:
            websocket (WebSocket): An instance of FastAPI WebSocket.

        Returns:
            dict: A message data in the form of a dictionary if the data is valid.
        """
        try:
            return await websocket.receive_json()
        except (JSONDecodeError, RuntimeError):
            await websocket.send_json({'title': 'Data integrity error.', 'details': 'Invalid JSON was provided.'})

    async def send(self, message_data: dict) -> None:
        """
        Send a message to a user if such is connected to the hub.

        Args:
            message_data (dict): A message in the form of a dictionary.
        """
        if (websocket := self.connections.get(message_data.get('recipient_id'))) is not None:
            await websocket.send_json(message_data)

    async def disconnect(self, user_id: int) -> None:
        """
        Close the websocket connection and remove the mapping from the storage.

        Args:
            user_id (int): An id of a user that has disconnected from the websocket endpoint.
        """
        if (websocket := self.connections.pop(user_id)) is not None:
            await websocket.close()
