







from json import JSONDecodeError
from uuid import uuid4

from fastapi import WebSocket

from application.ports import WebSocketHubPort
from infrastructure.monitoring import websocket_hub_active_connections


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
        websocket_id = uuid4().hex
        websocket.scope.update({'websocket_id': websocket_id})

        await websocket.accept()

        connections = self.connections.setdefault(user_id, set())
        connections.add(websocket)

        websocket_hub_active_connections.add(amount=1)

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

    async def send(self, message_data: dict, user_ids: set) -> None:
        """
        Send a message to a user if such is connected to the hub.

        Args:
            message_data (dict): A message in the form of a dictionary.
        """
        print(f'GOT USER IDS {user_ids}')
        for user_id in user_ids:
            if (websockets := self.connections.get(user_id)) is not None:
                print(f'CONNECTED WEBSOCKETS ARE {websockets}')
                for websocket in websockets:
                    await websocket.send_json(message_data)

    async def disconnect_user(self, user_id: int, websocket: WebSocket) -> None:
        """
        Close the websocket connection and remove the mapping from the storage.

        Args:
            user_id (int): An id of a user that has disconnected from the websocket endpoint.
            websocket (WebSocket): An instance of FastAPI WebSocket.
        """
        websocket_id = websocket.scope.get('websocket_id')

        if (websockets := self.connections.get(user_id)) is not None:

            websocket = next(iter(ws for ws in websockets if ws.scope.get('websocket_id') == websocket_id), None)

            if websocket is not None:
                websockets.remove(websocket)

                if not websockets:
                    self.connections.pop(user_id)

                websocket_hub_active_connections.add(amount=-1)
