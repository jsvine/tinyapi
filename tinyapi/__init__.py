from .session import Session

VERSION_TUPLE = (0, 0, 0)
VERSION = ".".join(map(str, VERSION_TUPLE))

def login(username, password):
    return Session(username, password)
