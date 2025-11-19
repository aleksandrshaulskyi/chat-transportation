from enum import Enum


class MessageStatus(str, Enum):
    """
    Represents the current delivery state of a message
    within the chat system.
    """
    SENT = 'sent'
    DELIVERED = 'delivered'
    REJECTED = 'rejected'
