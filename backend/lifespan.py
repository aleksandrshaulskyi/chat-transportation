from asyncio import CancelledError, create_task
from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.dependency_injector import DependenciesContainer
from infrastructure.tasks.consume_and_send_to_user import consume_and_send_to_user


@asynccontextmanager
async def lifespan(application: FastAPI):
    dependecies_container = DependenciesContainer()
    dependecies_container.wire(
        modules=[
            'infrastructure.dependencies.authentication',
            'infrastructure.handlers.messages',
            'infrastructure.tasks.consume_and_send_to_user',
            'infrastructure.websocket_hub.websocket_hub',
        ],
    )

    await dependecies_container.rabbitmq_manager().start()

    consumption_task = create_task(consume_and_send_to_user())

    try:
        yield
    finally:
        try:
            consumption_task.cancel()
        except CancelledError:
            pass

        await dependecies_container.rabbitmq_manager().close()
