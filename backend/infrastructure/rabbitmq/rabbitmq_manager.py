







from asyncio import CancelledError, create_task, QueueFull
from contextlib import suppress
from json import dumps

from aio_pika import AMQPException as AioPikaException, connect_robust, Exchange, ExchangeType, Message
from aiormq import AMQPException as AioRMQException

from settings import settings

from application.ports import RabbitMQManagerPort
from infrastructure.rabbitmq import RabbitMQDecoder
from infrastructure.transport import message_queue


class RabbitMQManager(RabbitMQManagerPort):
    """
    The RabbitMQ manager that is responsible for orchestrating RabbitMQ workflow.

    Specifically for:
    - Starting the connection and ensuring the excistence of exchanges.
    - Starting the consumption process for a user.
    - Creating and sending messages.
    - Closing the connection.
    """

    def __init__(self) -> None:
        """
        Initialize the manager.
        """
        self.connection = None
        self.publishing_channel = None
        self.websockets_exchange: Exchange = None
        self.database_exchange: Exchange = None
        self.user_channels = {}
        self.user_tasks = {}

    async def start(self) -> None:
        """
        Start the workflow. Create connection, single publishing channel and exchanges.
        """
        self.connection = await connect_robust(settings.rabbitmq_url)
        self.publishing_channel = await self.connection.channel(publisher_confirms=True)

        self.websockets_exchange = await self.publishing_channel.declare_exchange(
            name=settings.websockets_exchange_name,
            type=ExchangeType.DIRECT,
            passive=True,
        )

        self.database_exchange = await self.publishing_channel.declare_exchange(
            name=settings.database_exchange_name,
            type=ExchangeType.DIRECT,
            passive=True,
        )

    async def prepare_and_consume(self, user_id: int) -> None:
        """
        Prepare user channel for consumption from RabbitMQ, create the ephemeral queue,
        bind it to the exchange and start consumption process.

        Close the channel and unbind the task upon user disconnect.
        """
        try:
            user_channel = await self.connection.channel()
            await user_channel.set_qos(prefetch_count=settings.channel_prefetch_messages_count)

            self.user_channels.update({user_id: user_channel})

            user_queue = await user_channel.declare_queue(
                name=f'websocket.connection.{user_id}',
                exclusive=True,
                auto_delete=True,
                durable=False,
            )

            await user_queue.bind(self.websockets_exchange, str(user_id))

            async with user_queue.iterator() as queue_iterator:
                async for message in queue_iterator:
                    try:
                        async with message.process(requeue=False):
                            decoded_message = await RabbitMQDecoder(message=message.body).decode()
                            await message_queue.put(decoded_message)
                    except QueueFull:
                        await message.nack(requeue=True)
        except (AioPikaException, AioRMQException):
            pass  #duct tape until proper logging and reconnect
        except CancelledError:
            raise
   
    async def start_consumption_process(self, user_id: int) -> None:
        """
        Wrapper over prepare_and_consume method that creates an asyncio task.

        Args:
            user_id (int): The id of a user whom the task is being created for.
        """
        task = create_task(self.prepare_and_consume(user_id=user_id))
        self.user_tasks.update({user_id: task})

    async def stop_consumption_process(self, user_id: int) -> None:
        """
        Stop the consumption process.

        Cancel the consumption task if such exists and close the channel if it is not closed.
        """
        task = self.user_tasks.pop(user_id)
        channel = self.user_channels.pop(user_id)

        if task is not None:
            task.cancel()

        if channel is not None:
            with suppress(Exception):
                await channel.close()

    def create_message(self, body: bytes) -> Message:
        """
        Create a RabbitMQ message.

        Args:
            body (bytes): A message body.
        
        Returns:
            Message: An instance of RabbitMQ Message.
        """
        return Message(body=body, content_type='application/json', content_encoding='utf-8')

    async def send_message(self, message_data: dict) -> None:
        """
        Send message to the exchange.

        Dump and encode message data in the dictionary form, call the method to create an instance of
        RabbitMQ Message and publish it to the respectful exchange.

        Args:
            message_data (dict): A dictionary containing all the needed info to create a Message.
        """
        body = dumps(message_data).encode('utf-8')
        rabbitmq_message = self.create_message(body=body)
        await self.database_exchange.publish(message=rabbitmq_message, routing_key='')

    async def close(self) -> None:
        """
        Close the connection to RabbitMQ.
        """
        if self.publishing_channel and not self.publishing_channel.is_closed:
            await self.publishing_channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
