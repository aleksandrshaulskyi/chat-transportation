







from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from application.use_cases import ConnectUserUseCase
from infrastructure.dependencies import retrieve_user_id, retrieve_user_id_from_pass
from infrastructure.dependency_injector import DependenciesContainer
from infrastructure.incoming_dtos import IncomingMessageDTO
from infrastructure.rabbitmq import RabbitMQManager
from infrastructure.redis import RedisManager
from infrastructure.security import ConnectionPassManager
from infrastructure.websocket_hub import WebSocketHub
from interface_adapters.outgoing_dtos import OutgoingConnectionPassDTO
from interface_adapters.controllers import IssueConnectionPassController, SendMessageController


messages_router = APIRouter(prefix='/messages')

@messages_router.websocket('/')
@inject
async def send_message(
    websocket: WebSocket,
    user_id: int = Depends(retrieve_user_id_from_pass),
    websocket_hub: WebSocketHub = Depends(Provide[DependenciesContainer.websocket_hub]),
    rabbitmq_manager: RabbitMQManager = Depends(Provide[DependenciesContainer.rabbitmq_manager]),
) -> None:
    """
     Process websocket connections.

    - Connect user.
    - Receive messages.
    - Send messages to broker.
    - Disconnect user.
    """

    try:
        await ConnectUserUseCase(
            user_id=user_id,
            websocket=websocket,
            websocket_hub=websocket_hub,
            rabbitmq_manager=rabbitmq_manager,
        ).execute()

        while True:
            message_data = await websocket_hub.receive(websocket=websocket)

            try:
                incoming_message = IncomingMessageDTO(**message_data).model_dump()
            except ValidationError as exception:
                await websocket.send_json(
                    {
                        'title': 'Data consistency error.',
                        'details': exception.errors(),
                    }
                )
            else:

                controller = SendMessageController(
                    sender_id=user_id,
                    incoming_message=incoming_message,
                    rabbitmq_manager=rabbitmq_manager,
                )

                await controller.send_message()
    except WebSocketDisconnect:
        await websocket_hub.disconnect(user_id=user_id)
        await rabbitmq_manager.stop_consumption_process(user_id=user_id)

@messages_router.post('/get-connection-pass')
@inject
async def get_connection_pass(
    user_id: int = Depends(retrieve_user_id),
    connection_pass_manager: ConnectionPassManager = Depends(Provide[DependenciesContainer.connection_pass_manager]),
    redis_manager: RedisManager = Depends(Provide[DependenciesContainer.redis_manager]),
) -> OutgoingConnectionPassDTO:
    """
    Issues a one time connection pass to connect to the websocket endpoint.

    Returns:
        OutgoingConnectionPassDTO: The dataclass containing connection_pass.
    """

    controller = IssueConnectionPassController(
        user_id=user_id,
        connection_pass_manager=connection_pass_manager,
        redis_manager=redis_manager,
    )

    return await controller.issue_connection_pass()
