from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Object, Singleton

from infrastructure.rabbitmq import RabbitMQManager
from infrastructure.redis import RedisManager
from infrastructure.security import ConnectionPassManager
from infrastructure.websocket_hub import WebSocketHub


class DependenciesContainer(DeclarativeContainer):
    """
    The main dependency container of the infrastructure layer.

    It defines and manages singletons for the infrastructure-level components:
    RabbitMQ connection, Redis connection, WebSocket hub, and connection pass manager.
    """

    process_id = Object(None)

    rabbitmq_manager = Singleton(RabbitMQManager, process_id=process_id)
    """
    Manages RabbitMQ connections and publishing/consumption channels.
    """

    redis_manager = Singleton(RedisManager, process_id=process_id)
    """
    Handles operations with Redis.
    """
    websocket_hub = Singleton(WebSocketHub)
    """
    Tracks active WebSocket connections and their user bindings.
    """

    connection_pass_manager = Singleton(ConnectionPassManager)
    """
    Issues temporary connection passes for WebSocket authentication.
    """
