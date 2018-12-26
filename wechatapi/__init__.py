from .first_access import __init__, bp
from .token import access

def init(config):
    __init__(config)
    return access(config)

