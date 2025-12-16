from asyncio import CancelledError, create_task
from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.dependency_injector import DependenciesContainer
from infrastructure.tasks import consume_and_send_to_user
from infrastructure.utils import generate_process_id


@asynccontextmanager
async def lifespan(application: FastAPI):
    process_id = generate_process_id()

    dependecies_container = DependenciesContainer(process_id=process_id)
    dependecies_container.wire(
        modules=[
            'infrastructure.dependencies.authentication',
            'infrastructure.handlers.messages',
            'infrastructure.tasks.consume_and_send_to_user',
            'infrastructure.websocket_hub.websocket_hub',
        ],
    )

    rabbitmq_manager = dependecies_container.rabbitmq_manager()

    await rabbitmq_manager.start()

    rabbitmq_consumption_task = create_task(rabbitmq_manager.consume())
    queue_consumption_task = create_task(consume_and_send_to_user())

    try:
        yield
    finally:
        try:
            rabbitmq_consumption_task.cancel()
        except CancelledError:
            pass

        await dependecies_container.rabbitmq_manager().close()
