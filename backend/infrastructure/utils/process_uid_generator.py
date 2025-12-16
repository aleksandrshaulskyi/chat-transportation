"""
The module that implemets simple unique id generator.
"""
from secrets import token_hex


def generate_process_id() -> str:
    """
    Generate a 16 bytes unique process id that will allow us to identify
    the process to dispatch messages.
    """
    return token_hex(16)
