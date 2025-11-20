from fastapi import FastAPI

from infrastructure.handlers import setup_routers
from infrastructure.middleware import setup_middleware
from lifespan import lifespan


def compose_application() -> FastAPI:
    """
    Compose the application.

    - Setup routers.
    - Setup middleware

    Returns:
        FastAPI: An instance of FastAPI application.
    """
    application = FastAPI(lifespan=lifespan, root_path='/transportation')

    setup_routers(application=application)
    setup_middleware(application=application)

    return application
