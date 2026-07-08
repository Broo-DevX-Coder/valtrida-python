from .market import redirect_connection_errors
from .market import SINGLE_API

listeners = [redirect_connection_errors]
CHOISED_SYMBOLS_CLASS = SINGLE_API