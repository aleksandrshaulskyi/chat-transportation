from redis.asyncio import from_url

from settings import settings


class RedisManager:
    """
    The Redis manager.

    Responsible for orchestrating the workflow with Redis.
    """

    def __init__(self, process_id: str) -> None:
        """
        Initialize the manager.

        Args:
            process_id (str): A string that identifies the process and allows to dispatch messages.
        """
        self.redis = from_url(url=settings.redis_url, decode_responses=True, encoding='utf-8')
        self.process_id = process_id

    async def map_connection(self, user_id: int) -> None:
        """
        Map a connection of a user to the websocket hub shard.

        When connected the k: v pair of user id and process id is stored in Redis
        for further message routing.
        """
        await self.redis.sadd(f'connections:user:{user_id}', self.process_id)

    async def remove_mapping(self, user_id: int) -> None:
        """
        Remove previously mapped connection from the Redis.
        """
        await self.redis.srem(f'connections:user:{user_id}', self.process_id)

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
