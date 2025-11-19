







from dataclasses import asdict, dataclass
from datetime import datetime

from settings import settings

from domain.value_objects import MessageStatus


@dataclass
class Message:
    """
    Domain entity representing a chat message.

    This object is created when a user sends a message.
    It can be persisted in the database and transferred
    across services (e.g. from transport to storage).

    Attributes:
        id (int | None): Primary database identifier (None for unsaved messages).
        client_message_id (str): Client-generated unique message ID for idempotency.
        chat_id (str | None): Chat identifier (may be assigned later by storage service).
        sender_id (int): ID of the user who sent the message.
        recipient_id (int): ID of the user receiving the message.
        status (MessageStatus): Delivery status (e.g., SENT, DELIVERED, READ).
        sent_at (datetime): Timestamp when message was sent.
        delivered_at (datetime | None): Timestamp when message was delivered.
        body (str): The actual message text.
        is_edited (bool): Whether the message was edited.
        is_deleted (bool): Whether the message was deleted.
    """
    id: int | None
    client_message_id: str
    chat_id: str | None
    sender_id: int
    recipient_id: int
    status: MessageStatus
    sent_at: datetime
    delivered_at: datetime | None
    body: str
    is_edited: bool
    is_deleted: bool

    @property
    def representation(self) -> dict:
        """
        Convert the message entity into a serializable dictionary.

        Used for JSON serialization and sending through RabbitMQ.

        Returns:
            dict: The serializible representation of the Message entity.
        """
        return asdict(self)

    @classmethod
    def create(cls, message_data: dict) -> 'Message':
        """
        Factory method for constructing a new Message entity.

        Args:
            message_data (dict): Clean validated data from the application layer.

        Returns:
            Message: A new Message object.
        """
        return Message(
            id=None,
            client_message_id=message_data.get('client_message_id'),
            chat_id=message_data.get('chat_id'),
            sender_id=message_data.get('sender_id'),
            recipient_id=message_data.get('recipient_id'),
            status=MessageStatus.SENT,
            sent_at=datetime.strftime(datetime.now(), settings.default_datetime_format),
            delivered_at=None,
            body=message_data.get('body'),
            is_edited=False,
            is_deleted=False,
        )
