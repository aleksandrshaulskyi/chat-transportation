from fastapi import FastAPI

from infrastructure.handlers import setup_routers
from infrastructure.middleware import setup_middleware
from infrastructure.monitoring import setup_metrics
from lifespan import lifespan


def compose_application() -> FastAPI:
    """
    Compose the application.

    - Setup routers.
    - Setup middleware.
    - Setup metrics.

    Returns:
        FastAPI: An instance of FastAPI application.
    """
    application = FastAPI(lifespan=lifespan, root_path='/transportation')

    setup_routers(application=application)
    setup_middleware(application=application)
    setup_metrics(application=application)

    return application
