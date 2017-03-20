from .session import Session
from .draft import Draft

def login(username, password):
    """Create a TinyAPI session."""
    return Session(username, password)
