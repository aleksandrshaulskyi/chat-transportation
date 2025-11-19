from asyncio import CancelledError

from dependency_injector.wiring import inject, Provide

from infrastructure.dependency_injector import DependenciesContainer
from infrastructure.transport import message_queue
from infrastructure.websocket_hub import WebSocketHub


@inject
async def consume_and_send_to_user(
    websocket_hub: WebSocketHub = Provide[DependenciesContainer.websocket_hub],
) -> None:
    """
    Consumes messages from the queue and then calls websocket hub to send messages to users.
    """

    try:
        while True:
            message_data = await message_queue.get()
            await websocket_hub.send(message_data=message_data)
    except CancelledError:
        raise
