from jwt import decode, PyJWTError

from settings import settings

from infrastructure.exceptions import AuthenticationException


class JWTManager:
    """
    The JSON Web Token Manager that orchestrates the workflow with tokens.
    """

    async def retrieve_user_id(self, token: str) -> None:
        """
        Decode a token. Verify it's validity and extract a user_id that should be stored in the payload
        section of a token.

        Args:
            token (str): A JWT.

        Returns:
            user_id (int): An id of a user if the token is valid and such was stored in the payload.
        
        Raises:
            AuthenticationException: Raisen if a token was invalid or user_id is not in the payload.
        """
        try:
            payload = decode(jwt=token, key=settings.key, algorithms=[settings.algorithm])
        except PyJWTError:
            raise AuthenticationException(
                title='Authentication exception.',
                details={'non-field-error': 'An invalid token was provided.'},
            )

        if (user_id := payload.get('user_id')) is not None:
            return user_id
        raise AuthenticationException(
            title='Authentication exception.',
            details={'non-field-error': 'Invalid payload in the token.'},
        )
