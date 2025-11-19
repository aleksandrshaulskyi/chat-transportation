from application.ports import ConnectionPassManagerPort, RedisManagerPort
from application.use_cases import IssueConnectionPassUseCase
from interface_adapters.outgoing_dtos import OutgoingConnectionPassDTO


class IssueConnectionPassController:
    """
    Orchestrates issuing a connection pass.

    This controller delegates the actual issuing to the corresponding use case
    and returns it in the appropriate format.
    """

    def __init__(
        self,
        user_id: int,
        connection_pass_manager: ConnectionPassManagerPort,
        redis_manager: RedisManagerPort,
    ) -> None:
        """
        Initialize class.

        Args:

            user_id (int): The id of the user that requested a connection pass.
            connection_pass_manager (ConnectionPassManager): The port for the connection pass manager.
            redis_manager (RedisManager): The port for the redis manager class.
        """
        self.user_id = user_id
        self.connection_pass_manager = connection_pass_manager
        self.redis_manager = redis_manager

    async def issue_connection_pass(self) -> OutgoingConnectionPassDTO:
        """
        Calls the use case and returns the connection pass in the
        format that is appropriate for the infrastructure layer.

        Returns:
            OutgoingConnectionPassDTO: The dataclass containing connection_pass.
        """
        use_case = IssueConnectionPassUseCase(
            user_id=self.user_id,
            connection_pass_manager=self.connection_pass_manager,
            redis_manager=self.redis_manager,
        )

        connection_pass = await use_case.execute()

        return OutgoingConnectionPassDTO(connection_pass=connection_pass)
