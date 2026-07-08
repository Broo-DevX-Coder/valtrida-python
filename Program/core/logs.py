# ==================================================================
# Import nessary modules
# ==================================================================

# == Libs ==
import asyncio
from datetime import datetime
import logging
import os
from rich.logging import RichHandler
import warnings

# == Local ==
from base.files_folders import APP_DATA
from .async_controller import LogsStream,SystemStream
from config import DEBUG_MODE

# == Set QT Library for PyQtGraph ==
os.environ["PYQTGRAPH_QT_LIB"] = "PySide2"

# == Logs file setup ==
LOGS_FILE = os.path.join(APP_DATA,"logs/")
os.makedirs(LOGS_FILE,exist_ok=True)

# logging place ============================================================
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE is True else logging.INFO,               # Minimum level to log 
    handlers=[
        logging.FileHandler(filename=os.path.join(LOGS_FILE,str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+".log"),mode="w"), # To Save evry thing in the log file
        RichHandler()
    ],
    format="%(asctime)s [%(levelname)s] -> %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S",       # Date/time format
    style='%'                          # Format style (default is '%', can use '{')
)


# Log that logging is ready
logging.debug("Logging is ready")

# Set logging level for external libraries to CRITICAL to avoid cluttering the logs with unnecessary information
logging.getLogger("websockets").setLevel(logging.CRITICAL)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("qasync").setLevel(logging.CRITICAL)
logging.getLogger("socket").setLevel(logging.CRITICAL)
logging.getLogger("pyside2").setLevel(logging.CRITICAL)
logging.getLogger("uniquant").setLevel(logging.CRITICAL)


# Filter out specific warnings that are not relevant to the user and can be safely ignored
# warnings.filterwarnings("ignore", message=".*Task was destroyed but it is pending!*")
# warnings.filterwarnings("ignore", message=".*Item already added to PlotItem, ignoring.*")
# warnings.filterwarnings("ignore", category=RuntimeWarning, message="coroutine.*never awaited")


# == Listeners for LogsStream ==
async def logs_listener():
    """
    Listen to the LogsStream for messages related to logs, such as trade logs, system logs, etc.
    """
    sub = LogsStream.subscribe("all")
    while True:
        message = await sub.get()
        mtype = str(message["type"])
        content = str(message["payload"]["content"])
        source = str(message["source"]) if DEBUG_MODE is True else "Unknown"
        source_component = f"[{source}] -> " if source != "Unknown" else ""

        if mtype == "debug" and DEBUG_MODE is True:
            logging.debug(f"{source_component}{content}")
        elif mtype == "warning" and DEBUG_MODE is True:
            logging.warning(f"{source_component}{content}")
        elif mtype == "info":
            logging.info(f"{source_component}{content}")

# == Listeners for SystemStream ==
async def system_logs_listener():
    """
    Listen to the LogsStream for messages related to logs, such as trade logs, system logs, etc.
    """
    sub = SystemStream.subscribe("all")
    while True:
        message = await sub.get()
        mtype = str(message["type"])
        is_headen = False
        content = str(message["event"]) if "event" not in message["payload"] else str(message["payload"]["event"])
        source = str(message["source"]) if DEBUG_MODE is True else "Unknown"
        source_component = f"[{source}]" if source != "Unknown" else ""

        if "headen" in message["payload"]:
            if bool(message["payload"]["headen"]) is True:
                is_headen = True
        
        if is_headen is True and DEBUG_MODE is False:
            continue
        logging.info(f"{source_component}[{mtype}] -> {content}")

# == Log function ==
def log(ltype:str,content:str,source:str=""):
    """
    Send a log message to the LogsStream with the specified type, content, and source.
    """
    asyncio.create_task(LogsStream.put({
        "type": ltype,
        "event": "log",
        "source": source,
        "time": datetime.now().timestamp(),
        "payload": {
            "content": content
        }
    }))
