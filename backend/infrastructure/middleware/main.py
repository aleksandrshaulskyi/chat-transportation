from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from settings import settings


def setup_middleware(application: FastAPI) -> None:
    """
    Setup the application middleware.
    """
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
