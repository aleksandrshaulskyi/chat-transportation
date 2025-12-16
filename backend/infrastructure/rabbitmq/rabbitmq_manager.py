from asyncio import CancelledError, QueueFull
from logging import getLogger
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

    def __init__(self, process_id: str) -> None:
        """
        Initialize the manager.

        Args:
            process_id (str): A string that identifies the process where an instance of this manager currently runs.
        """
        self.process_id = process_id
        self.connection = None
        self.publishing_channel = None
        self.consumption_channel = None
        self.websockets_exchange: Exchange = None
        self.database_exchange: Exchange = None
        self.logger = getLogger(settings.messages_logger_name)

    async def start(self) -> None:
        """
        Start the workflow. 
        - Create connection, 
        - Create publishing and consumption channels.
        - Create exchanges.
        """
        self.connection = await connect_robust(settings.rabbitmq_url)

        self.publishing_channel = await self.connection.channel(publisher_confirms=True)
        self.consumption_channel = await self.connection.channel()

        await self.consumption_channel.set_qos(prefetch_count=settings.channel_prefetch_messages_count)

        self.database_exchange = await self.publishing_channel.declare_exchange(
            name=settings.database_exchange_name,
            type=ExchangeType.DIRECT,
            passive=True,
        )

        self.websockets_exchange = await self.consumption_channel.declare_exchange(
            name=settings.websockets_exchange_name,
            type=ExchangeType.DIRECT,
            passive=True,
        )

    async def consume(self) -> None:
        """
        Consume from websockets exchange.

        - Create the process queue.
        - Bind the queue.
        - Consume messages from RabbitMQ.
        """
        print('CONSUMING')
        try:
            process_queue = await self.consumption_channel.declare_queue(
                name=f'websocket.{self.process_id}',
                durable=False,
                exclusive=True,
            )

            await process_queue.bind(self.websockets_exchange, self.process_id)

            async with process_queue.iterator() as queue_iterator:
                async for message in queue_iterator:
                    try:
                        async with message.process(requeue=False):
                            decoded_message = await RabbitMQDecoder(message=message.body).decode()
                            await message_queue.put(decoded_message)
                    except QueueFull:
                        await message.nack(requeue=True)
        except (AioPikaException, AioRMQException) as exception:
            self.logger.error(
                'RabbitMQ ephemeral queue error.',
                extra={'user_id': None, 'event_type': f'Queue connection error: {exception}'},
            )
        except CancelledError:
            raise

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
