from dataclasses import dataclass


@dataclass
class OutgoingConnectionPassDTO:
    """
    The dataclass that is used to return a connection pass to the user.
    """
    connection_pass: str
