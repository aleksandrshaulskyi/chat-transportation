from application.ports import ConnectionPassManagerPort, RedisManagerPort


class IssueConnectionPassUseCase:
    """
    Issue a connection pass that will allow to connect to the websocket endpoint once.
    """

    def __init__(
        self,
        user_id,
        connection_pass_manager: ConnectionPassManagerPort,
        redis_manager: RedisManagerPort,
    ) -> None:
        """"
        Initialize class.

        Args:
            user_id (int): The id of the user that requested a connection pass.
            connection_pass_manager (ConnectionPassManager): The port for the connection pass manager.
            redis_manager (RedisManager): The port for the redis manager class.
        """
        self.user_id = user_id
        self.connection_pass_manager = connection_pass_manager
        self.redis_manager = redis_manager

    async def execute(self) -> str:
        """
        Issue a single usage connection pass and add it to the redis.

        Returns:
            connection_pass (str): A connection pass.
        """
        connection_pass = await self.connection_pass_manager.issue_pass()
        await self.redis_manager.add_connection_pass(connection_pass=connection_pass, user_id=self.user_id)

        return connection_pass
