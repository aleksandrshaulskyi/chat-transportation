from abc import ABC, abstractmethod


class RabbitMQManagerPort(ABC):
    """
    The port for orchestrating messenging pipeline in RabbitMQ.
    """

    @abstractmethod
    async def prepare_and_consume(self, user_id: int) -> None:
        """
        This method is responsible for the preparation of user channels and ephemeral queues.
        
        It should create a channel, bind the queue to the exchange, consume from the queue
        and send messages to the internal messeging queue. It also should safely close channel
        and cancel the consumption upon user disconnect.

        Args:
            user_id (int): The id of the user that all the above things should be done for.
        """
        ...

    @abstractmethod
    async def start_consumption_process(self, user_id: int) -> None:
        """
        This method is responsible for the creation of an asyncio task for the previous method.
        
        Args:
            user_id (int): The id of the user that we create the task for.

        """
        ...

    @abstractmethod
    async def send_message(self, message_data: dict) -> None:
        """
        This method is responsible for sending the messages to the RabbitMQ.

        Args:
            message_data (dict): The serializable representation of a Message entity.
        """
        ...
