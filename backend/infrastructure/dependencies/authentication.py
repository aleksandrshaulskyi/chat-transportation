from http import HTTPStatus

from dependency_injector.wiring import inject, Provide
from fastapi import Depends, HTTPException, WebSocket, WebSocketException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from settings import settings

from infrastructure.dependency_injector import DependenciesContainer
from infrastructure.exceptions import AuthenticationException
from infrastructure.redis import RedisManager
from infrastructure.security import JWTManager


async def retrieve_user_id(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> int | None:
    """
    Retrieve the requesting user_id from authorization header.

    Returns:
        int: The requesting user_id if credentials provided are valid.

    Raises:
        HTTPException: If the credentials are missing or invalid.
    """
    if not (access_token := credentials.credentials):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='No token was provided.'
        )
    
    try:
        return await JWTManager().retrieve_user_id(token=access_token)
    except AuthenticationException as exception:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=exception.representation,
        )

@inject
async def retrieve_user_id_from_pass(
    websocket: WebSocket,
    redis_manager: RedisManager = Depends(Provide[DependenciesContainer.redis_manager]),
) -> int | None:
    """
    Retrieve the requesting user_id from a custom connection pass.

    Returns:
        int: The requesting user_id if credentials provided are valid.

    Raises:
        HTTPException: If the credentials are missing or invalid.
    """
    if (connection_pass := websocket.query_params.get('connection_pass')) is not None:
        if (user_id := await redis_manager.retrieve_user_id_from_pass(connection_pass=connection_pass)) is not None:
            return int(user_id)

    raise WebSocketException(code=settings.standard_unauthenticated_code)
