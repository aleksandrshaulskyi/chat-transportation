from secrets import choice
from string import ascii_letters, digits

from settings import settings


class ConnectionPassManager:
    """
    The connection pass manager.

    Responsible for issuing a unique tokens that are used to authenticate user upon connection
    to the websocket endpoint.
    """

    async def issue_pass(self) -> str:
        """
        Issue a unique token.
        """
        pool = ascii_letters + digits
        return ''.join(choice(pool) for _ in range(int(settings.connection_pass_length)))
