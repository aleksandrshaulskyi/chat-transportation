from asyncio import Queue

# Global asyncio queue that temporarily stores decoded messages
# received from RabbitMQ before they are dispatched to users.
message_queue = Queue()
