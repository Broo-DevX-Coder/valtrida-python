# ==================================================================
# Import nessary modules
# ==================================================================

# == Libs ==
from datetime import datetime
import logging

# == Local ==
from .async_controller import ErrorsStream,CRITICAL_STOP
from .pop_messages import pup_message
from config import DEBUG_MODE
from base.utils import NO_INTERNET_EXEPTIONS


# ==============================================================
# Listners functions to listen to the ErrorsStream for specific error events and handle them accordingly
# ==============================================================

# == Listeners for ErrorsStream ==
async def critical_errors_listener():
    """
    Listen to the ErrorsStream for messages related to errors, such as API errors, network errors, etc.
    """
    sub = ErrorsStream.subscribe("connection_error")
    while True:
        message = await sub.get()
        mtype = message.get("type", "")
        source = message.get("source", "Unknown") if DEBUG_MODE else ""

        if mtype.startswith("CONNECTION_429"):
            logging.error(f"[{source}]" if source != '' else ''+f"-> Too many requests (429). Please wait just 1 minute to retry\nif you dont wait, you IP ADress will blocked")
            pup_message("Too many requests","⚠️ Too many requests (429). Please wait just 1 minute to retry\nif you dont wait, you IP Adress will blocked",CRITICAL_STOP,"error")

        elif mtype.startswith("CONNECTION_418"):
            logging.error(f"[{source}]" if source != '' else ''+f"-> IP is banned temporarily (418). Please wait 1 hour to retry\nif you dont wait, you IP ADress will blocked")
            pup_message("Too many requests","🚫 IP is banned temporarily (418). Please wait 1 hour to retry\nif you dont wait, you IP ADress will blocked",CRITICAL_STOP,"error")

        elif mtype.startswith("CONNECTION_403"):
            logging.error(f"[{source}]" if source != '' else ''+f"-> Forbidden (403). Your IP might be blocked. Please Try to use VPN or Proxy server")
            pup_message("Too many requests","❌ Forbidden (403). Your IP might be blocked. Please Try to use VPN or Proxy server",CRITICAL_STOP,"error")

        elif mtype.startswith("CONNECTION_0"):
            logging.error(f"[{source}]" if source != '' else ''+f"-> No Internet Connection")
            pup_message("No Internet Connection","❌ No Internet Connection\nPlease Try to connect and retry",CRITICAL_STOP,"error")


async def errors_listener():
    """
    Listen to general error messages from the ErrorsStream and log them for debugging purposes.
    """
    sub = ErrorsStream.subscribe("all")
    while True:
        try:
            message = await sub.get()
            content = str(message["payload"]["message"])
            source = str(message["source"]) if DEBUG_MODE is True else "Unknown"

            source_component = f"[{source}] -> " if source != "Unknown" else ""
            logging.error(f"{source_component}{content}")
        except Exception as e:
            pass

# ==============================================================
# Export the errors_listener function to be used in other parts of the application
# ==============================================================

# Send a critical error message to the ErrorsStream
def critical_error(ntype:str,source:str=""):
    """
    Send a log message to the ErrorsStream with the specified type, content, and source.
    ltype is formatted as "CONNECTION_{ntype}" where ntype is the type of connection error (e.g., 429, 418, 403, 0).
    source is optional and can be included for debugging purposes to indicate where the error originated from.
    """
    ltype = f"CONNECTION_{ntype}"
    ErrorsStream.send({
        "type": ltype,
        "event": "connection_error",
        "source": source,
        "time": datetime.now().timestamp()
    })

# Send a general error message to the ErrorsStream
def error(etype,source:str,msg:str,module_etype='UNKNOWN'):
    event_ = "general_error"
    if type(etype) != str:
        error_type = str(type(etype)).replace("<class '",'').replace("'>",'')
    elif etype == "UNKNOWN" and type(module_etype) != str:
        error_type = str(type(module_etype)).replace("<class '",'').replace("'>",'')
    else:
        error_type = etype

    if error_type in NO_INTERNET_EXEPTIONS:
        event_ = "connection_error"
        error_type = "CONNECTION_0"

    ErrorsStream.send({
        "type": error_type,
        "event": event_,
        "source": source,
        "time": datetime.now().timestamp(),
        "payload": {
            "message": msg
        }
    })