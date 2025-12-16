from abc import ABC, abstractmethod


class RedisManagerPort(ABC):
    """
    The port for Redis connection.
    """

    @abstractmethod
    async def map_connection(self, user_id: int) -> None:
        """
        This method is responsible for the mapping of user id to the process id of a shard
        which a user is connected to.
        """
        ...

    @abstractmethod
    async def remove_mapping(self, user_id: int) -> None:
        """
        This method is responsible for the removal of a previously added mapping.
        """
        ...

    @abstractmethod
    async def add_connection_pass(self, connection_pass: str, user_id: int) -> None:
        """
        This method is responsible for adding a connection pass to Redis so that a user id
        can be retrieved using the pass upon connecting to the websocket endpoint.
        Technically creates a key-value pair that looks like {connection_pass: user_id} in Redis.

        Args:
            connection_pass (str): A token that allows the user to connect to the websocket endpoint.
            user_id (int): The user id that should be retrieved upon connecting to the websocket endpoint.
        """
        ...
