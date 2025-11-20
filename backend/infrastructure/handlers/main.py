from fastapi import FastAPI

from infrastructure.handlers.messages import messages_router


def setup_routers(application: FastAPI) -> None:
    """
    Setup FastAPI routers.
    """
    application.include_router(messages_router)
