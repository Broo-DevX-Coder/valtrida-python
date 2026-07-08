import asyncio
import sys
from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtWebEngine import QtWebEngine
from PySide2.QtWidgets import QApplication
import qasync

# STEP 1: Set attribute FIRST
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# STEP 2: Initialize QtWebEngine
QtWebEngine.initialize()

# STEP 3: Create QApplication
app = QApplication(sys.argv)

# STEP 4: Create event loop AFTER QApplication
loop = qasync.QEventLoop(app)
asyncio.set_event_loop(loop)

async def main():
    import prepare
    from windows.main import MainWindow
    

    obj = MainWindow()
    obj.run()

    while True:
        await asyncio.sleep(1000)

if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    except (RuntimeError, KeyboardInterrupt):
        pass