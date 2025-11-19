from pydantic import BaseModel


class IncomingMessageDTO(BaseModel):
    """
    The DTO used to validate the incoming data that is sent via websockets
    to create messages.
    """
    client_message_id: str
    chat_id: str
    recipient_id: int
    body: str
