"""
Asynchronous programming utilities for the application, including async functions, event loops, and task management.
Streams for real-time data updates and communication between components.
"""

# ==================================================================
# Import nessary modules
# ==================================================================

# == Libs ==
import sys
import asyncio

# == local ==
from base.utils import QueueStreamChannel

# ==================================================================
# Streams
# ==================================================================
ErrorsStream = QueueStreamChannel()
UserStream = QueueStreamChannel()
LogsStream = QueueStreamChannel()
SystemStream = QueueStreamChannel()
"""
Exemple of message:
{
    "type": str,
    "event": str,
    "source": str,
    "time": float,
    "payload": dict
}
"""

# ==================================================================
# Vars
# ==================================================================
ALL_ASYNC_FUNCTIONS = []  # List to store all async functions for management and tracking
ALL_QT_WINDOWS = []  # List to store all Qt windows for management and tracking
ALL_REST_SESSIONS = []  # List to store all REST sessions for management and tracking
ALL_THREADS = []  # List to store all threads for management and tracking
ALL_ASYNC_LOOPS = []  # List to store all async loops for management and tracking

# ==================================================================
# functions
# ==================================================================

class AsyncController:
    """
    Controller class to manage async functions, threads, REST sessions, and windows in the application.
    it has 4 main functions to manage each type of resource
    they are: window_m, rest_m, async_m, thread_m
    """
    def window_m(window,event:str="add"):
        """
        Add a Qt window to the list of managed windows.
        This function is used to keep track of all open windows in the application for proper management and cleanup.
        """
        if event == "add" and window not in ALL_QT_WINDOWS:
            ALL_QT_WINDOWS.append(window)
        elif event == "delete" and window in ALL_QT_WINDOWS: 
            ALL_QT_WINDOWS.remove(window)
    
    def loop_m(loop,event:str="add"):
        """
        Add an async loop to the list of managed loops.
        This function is used to keep track of all running async loops in the application for proper management and cleanup.
        """
        if event == "add" and loop not in ALL_ASYNC_LOOPS:
            ALL_ASYNC_LOOPS.append(loop)
        elif event == "delete" and loop in ALL_ASYNC_LOOPS: 
            ALL_ASYNC_LOOPS.remove(loop)

    def rest_m(session,event:str="add"):
        """
        Add a REST session to the list of managed sessions.
        This function is used to keep track of all active REST sessions in the application for proper management and cleanup.
        """
        if event == "add" and session not in ALL_REST_SESSIONS:
            ALL_REST_SESSIONS.append(session)
        elif event == "delete" and session in ALL_REST_SESSIONS: 
            ALL_REST_SESSIONS.remove(session)

    def async_m(func,event:str="add"):
        """
        Add an async function to the list of managed functions.
        This function is used to keep track of all running async functions in the application for proper management and cleanup.
        """
        if event == "add" and func not in ALL_ASYNC_FUNCTIONS:
            ALL_ASYNC_FUNCTIONS.append(func)
        elif event == "delete" and func in ALL_ASYNC_FUNCTIONS: 
            ALL_ASYNC_FUNCTIONS.remove(func)

    def thread_m(thread,event:str="add"):
        """
        Add a thread to the list of managed threads.
        This function is used to keep track of all running threads in the application for proper management and cleanup.
        """
        if event == "add" and thread not in ALL_THREADS:
            ALL_THREADS.append(thread)
        elif event == "delete" and thread in ALL_THREADS: 
            ALL_THREADS.remove(thread)

# Stop everything
def CRITICAL_STOP():
    """
    Stop all async functions, threads, REST sessions, and close all windows immediately.
    This function is used in case of critical errors or when the application needs to be shut down quickly.
    """
    loop = asyncio.get_event_loop()

    # Close all Qt windows
    def close_window(y):
        try: 
            return y.close() 
        except: 
            pass
    loop.run_until_complete(asyncio.gather(*( close_window(i) for i in ALL_QT_WINDOWS)))

    # Cancel all async functions
    for i in ALL_ASYNC_FUNCTIONS:
        try:
            i.cancel()
        except:
            pass

    # Join all threads
    for i in ALL_THREADS:
        try:
            i.join(timeout=1)
        except:
            pass

    # Stop all async loops
    for i in ALL_ASYNC_LOOPS:
        try:
            i.call_soon_threadsafe(i.stop)
        except:
            pass

    # Close all REST sessions
    for i in ALL_REST_SESSIONS:
        try:
            loop.run_until_complete(i.close())
        except:
            pass

    sys.exit(1)