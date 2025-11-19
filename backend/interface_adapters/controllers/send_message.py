from application.ports import RabbitMQManagerPort
from application.use_cases import SendMessageUseCase


class SendMessageController:
    """
    Orchestrates sending a message through the messaging pipeline.

    This controller adapts incoming message data and delegates
    the actual sending to the corresponding use case.
    """

    def __init__(
        self,
        sender_id: int,
        incoming_message: dict,
        rabbitmq_manager: RabbitMQManagerPort,
    ) -> None:
        """
        Initialize the controller.

        Args:
            sender_id (int): The id of the user that has sent a message.
            incoming_message (dict): The dict containing message data.
            rabbitmq_manager (RabbitMQManagerPort): The port for RabbitMQ.
        """
        self.sender_id = sender_id
        self.incoming_message = incoming_message
        self.rabbitmq_manager = rabbitmq_manager

    async def send_message(self) -> None:
        """
        Get the prepared message data and call the use case
        in order to send a message to the broker.
        """
        clean_message_data = await self.prepare_message_data()

        use_case = SendMessageUseCase(
            message_data=clean_message_data,
            rabbitmq_manager=self.rabbitmq_manager,
        )

        await use_case.execute()

    async def prepare_message_data(self) -> dict:
        """
        Compose the data required by the use case.

        Returns:
            dict: The data that is required by the use case.
        """

        return {
            'client_message_id': self.incoming_message.get('client_message_id'),
            'chat_id': self.incoming_message.get('chat_id'),
            'sender_id': self.sender_id,
            'recipient_id': self.incoming_message.get('recipient_id'),
            'body': self.incoming_message.get('body'),
        }
