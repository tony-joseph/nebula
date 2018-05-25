from .base import *

DEBUG = True


try:
    from .local_settings import *
except ImportError:
    pass
