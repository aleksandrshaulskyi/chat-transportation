from application.ports import RabbitMQManagerPort
from domain.entities import Message


class SendMessageUseCase:
    """
    The use case that is responsible for creating the message entity and sending message
    to the RabbitMQ broker.
    """

    def __init__(
        self,
        message_data: dict,
        rabbitmq_manager: RabbitMQManagerPort,
    ) -> None:
        """
        Initialize the use case.

        Args:
            message_data (dict): The dictionary that contains all the needed message data.
            rabbitmq_manager (RabbitMQManagerPort): The port for RabbitMQ.
        """
        self.message_data = message_data
        self.rabbitmq_manager = rabbitmq_manager

    async def execute(self) -> None:
        """
        Creates the message and then sends it to RabbitMQ broker.
        """
        message = Message.create(self.message_data)

        await self.rabbitmq_manager.send_message(
            message_data=message.representation,
        )
