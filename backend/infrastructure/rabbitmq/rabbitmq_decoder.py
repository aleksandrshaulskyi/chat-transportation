from json import JSONDecodeError, loads
from logging import getLogger

from settings import settings


class RabbitMQDecoder:
    """
    The basic RabbitMQ messages decoder that is responsible for
    deserealizing messages from bytes to dict.
    """

    def __init__(self, message: bytes) -> None:
        """
        Initialize the decoder.

        Args:
            message (bytes): A message from RabbitMQ.
        """
        self.message = message
        self.logger = getLogger(settings.messages_logger_name)

    async def decode(self) -> dict | None:
        """
        Decode message.

        Returns:
            dict: A dictionary containing message data.

        Raises:
            AttributeError: Raisen if decoding was impossible.
            JSONDecodeError: Raisen if a messages con not be transformed into a valid JSON.
        """
        try:
            decoded_message_data = self.message.decode('utf-8')
        except AttributeError:
            self.logger.error(
                f'RabbitMQ message decoding error: {self.message}',
                extra={'user_id': None, 'event_type': 'String instead of bytes'},
            )
        else:

            try:
                clean_message_data = loads(decoded_message_data)
            except JSONDecodeError:
                self.logger.error(
                    f'RabbitMQ message json error: {self.message}',
                    extra={'user_id': None, 'event_type': 'Error while JSON parsing.'},
                )
            else:
                return clean_message_data
