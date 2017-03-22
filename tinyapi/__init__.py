from .session import Session
from .draft import Draft
from ._version import __version__

def login(username, password):
    """Create a TinyAPI session."""
    return Session(username, password)
