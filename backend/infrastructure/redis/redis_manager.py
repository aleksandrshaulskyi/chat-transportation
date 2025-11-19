from redis.asyncio import from_url

from settings import settings


class RedisManager:
    """
    The Redis manager.

    Responsible for orchestrating the workflow with Redis.
    """

    def __init__(self) -> None:
        """
        Initialize the manager.
        """
        self.redis = from_url(url=settings.redis_url, decode_responses=True, encoding='utf-8')
    
    async def add_connection_pass(self, connection_pass: str, user_id: int) -> None:
        """
        Add a key-value pair to Redis so that user_id can be
        retrieved upon connecting to the websocket endpoint.

        Args:
            connection_pass (str): The unique token that will be used as a key to retrieve user_id.
            user_id (int): The id of a user to authenticate him upon connection to the websocket endpoint.
        """
        await self.redis.set(connection_pass, str(user_id), ex=settings.connection_pass_expiration_time)

    async def retrieve_user_id_from_pass(self, connection_pass: str) -> str | None:
        """
        Retrieve previously stored connection_pass: user_id pair for user authentication
        and delete is as it is intended for the single use only.

        Args:
            connection_pass (str): A previously stored connection pass.
        Returns:
            str: A user_id related to the provided connection pass if such exists.
        """
        return await self.redis.getdel(name=connection_pass)
