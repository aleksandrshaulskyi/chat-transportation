from abc import ABC, abstractmethod


class RabbitMQManagerPort(ABC):
    """
    The port for orchestrating messenging pipeline in RabbitMQ.
    """

    @abstractmethod
    async def send_message(self, message_data: dict) -> None:
        """
        This method is responsible for sending the messages to the RabbitMQ.

        Args:
            message_data (dict): The serializable representation of a Message entity.
        """
        ...
