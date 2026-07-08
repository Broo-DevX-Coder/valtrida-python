# ==================================================================
# Import nessary modules
# ==================================================================

# ==libs ==
import asyncio
from functools import partial
import os
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

# == local ==
from Styles.qss import QSS
from base.files_folders import ASSETS_ICONS_ICO
from core import AsyncController,log,error,critical_error,UserStream,SystemStream


# == pages ==
from .widgets.login import LoggingWidget
from .widgets.register_via_binance_api import RegisterViaBinanceAPI

AUTH_OPTIONS = {
    'Login': LoggingWidget,
    'API Register':RegisterViaBinanceAPI
}
AUTH_OPTIONS_TOOLTIPS = {
    'Login':"Login via UserName/Email ...",
    'API Register':"Register via binance api and secreat key (hmac crypting)"
}



class AuthMain(QWidget):
    def __init__(self):
        super().__init__()
        self.size_ = [350, 170]
        self.setFixedSize(self.size_[0], self.size_[1])
        self.setWindowTitle("Valtrida")
        self.setStyleSheet(QSS["BINANCE"])
        self.setWindowIcon(QIcon(os.path.join(ASSETS_ICONS_ICO,"main.ico")))
        self.buttons_needed = []
        AsyncController.window_m(self,'add')

        # --- set stack -----
        self.stacked = QStackedWidget(self)
        self.stacked.setObjectName("options_stacked")
        self.stacked.setGeometry(0, 50, self.size_[0], self.size_[1]-50)

        # --- options bar ---
        self.options_bar = QWidget(self)
        self.options_bar.setObjectName("options_bar")
        self.options_bar.setGeometry(0,0,self.size_[0],50)
        self.options_bar.setStyleSheet(QSS["AUTH_TOOL_BAR"])

        layout = QHBoxLayout(self.options_bar)
        layout.setSpacing(4)

        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        # --- Creat button for eatch option ---
        self.options_buttons = {}
        for name,tooltip in AUTH_OPTIONS_TOOLTIPS.items():
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            self.group.addButton(btn)
            layout.addWidget(btn)
            btn.clicked.connect(partial(self.cahnge_window,name))
            self.options_buttons[name] = btn

        layout.addStretch()

        # --- add options windows in stacked ---
        self.stacked_windows = {}
        for name,obj in AUTH_OPTIONS.items():
            self.stacked_windows[name] = obj()
            self.stacked.addWidget(self.stacked_windows[name])

        # --- set login page the first one ---
        self.cahnge_window("Login")

    
    def cahnge_window(self,name):
        if name in self.stacked_windows.keys():
            curent_wdg = self.stacked_windows.get(name)
            self.stacked.setCurrentWidget(curent_wdg)
            self.setFixedSize(curent_wdg.size_[0],curent_wdg.size_[1]+50)
            self.stacked.setGeometry(0, 50, curent_wdg.size_[0], curent_wdg.size_[1]+50)

            for i,btn in self.options_buttons.items():
                btn.setChecked(False)
            self.options_buttons[name].setChecked(True)



    def closeEvent(self, event):
        event.accept()

    def run(self):
        self.show()

if __name__ == "__main__":
    import sys
    import qasync
    import core,API


    app = QApplication(sys.argv)
    loop = qasync.QEventLoop()

    async def main():
        for i in core.listeners: asyncio.create_task(i())
        for i in API.listeners: asyncio.create_task(i())
        obj__ = AuthMain()
        obj__.show()
        while True:
            await asyncio.sleep(1000)

    try:
        with loop:
            loop.run_until_complete(main())
    except (RuntimeError, KeyboardInterrupt):
        pass