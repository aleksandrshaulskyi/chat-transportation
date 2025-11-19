from abc import ABC, abstractmethod


class ConnectionPassManagerPort(ABC):
    """
    The port for issuing temporary connection passes to authenticated users.

    This abstraction hides the underlying mechanism that generates and stores
    temporary connection identifiers used by the transport layer.
    """

    @abstractmethod
    async def issue_pass(self) -> str:
        """
        Generate a connection pass.

        The pass must be:
            - unique across all active sessions;
            - short-lived (expires automatically after a configured TTL).

        Returns:
            str: The unique identifier (token) representing the issued pass.
        """
        ...
