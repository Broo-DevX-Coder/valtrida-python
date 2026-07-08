# ==================================================================
# Import nessary modules
# ==================================================================

# ==libs ==
import asyncio
import sys
import os
from functools import partial

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import aiohttp

# == local ==
from base.tool_bar import MW_STACKED_WINDOWS,MW_WINDOW_STAKED_BUTTONS,MW_POPUP_WIDOWS_BUTTONS,MW_POPUP_WIDOWS
from base.files_folders import ASSETS_ICONS_SVG,ASSETS_ICONS_ICO
from base.user_data import *

from core import AsyncController,log,error,critical_error,UserStream,SystemStream
from Styles.qss import QSS
from Program.API.account import get_total_balance_in_usdt
from .coin import OneCoin


# ==================================================================
# Helper classes and functions
# ==================================================================
def critical_error_(ntype:str,source:str=""):
    """
    Specific critical errors function for this file
    """
    critical_error(ntype, f"windows.main.{source}")

def error_(etype,source:str,msg:str):
    """
    Specific general errors function for this file
    """
    error(etype, f"windows.main.{source}", msg)

def log_(ltype:str,msg:str,source:str=""):
    """
    Specific log function for this file
    """
    log(ltype,msg, f"windows.main.{source}")

# ==== Overlay class ====
class OverlayPopup(QWidget):
    """Overlay popup with transparent background"""
    def __init__(self, parent:QWidget,content_widget:QWidget):
        super().__init__(parent)
        self.parent_window = parent
        
        # Make it cover the entire parent window
        self.setGeometry(parent.rect())
        self.setStyleSheet(QSS["BINANCE"])
        
        # Frameless and transparent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Widget)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Create a central widget for content (in the middle)
        self.content_widget = content_widget
        content_widget.setParent(self)
        self.content_widget.setStyleSheet(QSS["BINANCE"]+"\nQWidget { border-radius:5px; }")
        
        # Setup layout for content widget
        self.close_btn = QPushButton("Close",self)
        self.close_btn.setGeometry(10, self.height() - 70, (len(MW_WINDOW_STAKED_BUTTONS)+len(MW_POPUP_WIDOWS_BUTTONS))*62, 55)
        self.close_btn.show()
        self.close_btn.clicked.connect(self.hide)

        # Position content widget in the center
        self.center_content()
    
    def center_content(self):
        """Center the content widget in the overlay"""
        overlay_rect = self.rect()
        x = (overlay_rect.width() - self.content_widget.width()) // 2
        y = (overlay_rect.height() - self.content_widget.height()) // 2
        self.close_btn.setGeometry(10, self.height() - 70, (len(MW_WINDOW_STAKED_BUTTONS)+len(MW_POPUP_WIDOWS_BUTTONS))*62, 55)
        self.content_widget.move(x, y)
    
    def paintEvent(self, event):
        """Draw semi-transparent background"""
        painter = QPainter(self)
        # Semi-transparent black background (0, 0, 0, 128) = 50% opacity
        painter.fillRect(self.rect(), QColor(0, 0, 0, 180))
    
    def resizeEvent(self, event):
        """Update overlay size when parent resizes"""
        self.setGeometry(self.parent_window.rect())
        self.center_content()
        return super().resizeEvent(event)
    
    def showEvent(self, event):
        self.raise_()
        return super().showEvent(event)

    def run(self):
        self.content_widget.run()
    
    def specific_show(self,*args,**kewarg):
        self.content_widget.specific_show(*args,**kewarg)
        self.show()


# ==================================================================
# Main class
# ==================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.async_tasks = []
        self.windows = []

        self.logged_in = False

        size = [1100,800]
        self.setMinimumSize(size[0],size[1])
        self.set_window_t = lambda x: self.setWindowTitle(f"Valtrida - {USER_LOCAL_INFO['name']} - {x}" if USER_LOCAL_INFO['name'] != None and USER_LOCAL_INFO['name'] != "" else f"Valtrida - {x}")
        self.setWindowIcon(QIcon(os.path.join(ASSETS_ICONS_ICO,"main.ico")))
        self.set_window_t("Home")

        # Set Every var befor runing
        self.FIRST_MW_STACKED_WINDOWS = MW_STACKED_WINDOWS.copy()
        self.FIRST_MW_POPUP_WIDOWS = MW_POPUP_WIDOWS.copy()
        self.FIRST_MW_WINDOW_STAKED_BUTTONS = MW_WINDOW_STAKED_BUTTONS.copy()
        self.FIRST_MW_POPUP_WIDOWS_BUTTONS = MW_POPUP_WIDOWS_BUTTONS.copy()


        # Start the instance :) ---
        log_("info","Start main window","MainWindow.__init__")
        AsyncController.window_m(self,'add')

        # ===== Windows system ==========
        # Stacked windows
        self.stack = QStackedWidget(self)
        self.stcked_windows = {}
        for u,i in MW_STACKED_WINDOWS.items(): 
            self.stcked_windows[u] = i()
        self.stcked_windows_layouts = {}
        
        # pop-up windows
        self.popup_windows = {}
        for u,i in MW_POPUP_WIDOWS.items(): 
            g = i
            g["m"] = OverlayPopup(self,i["m"]())
            self.popup_windows[u] = g

        # ======= Create Toolbar =========
        self.tool_bar = {
            "w": QWidget(self),
            "geometry":[10, self.height() - 70, (len(MW_WINDOW_STAKED_BUTTONS)+len(MW_POPUP_WIDOWS_BUTTONS))*62, 55],
            "stacks":{},
            "pop-up":{}
        }

        self.tool_bar["w"].setStyleSheet(QSS["MAIN_W_TOOL_BAR"])

        self.tool_bar_layout = QHBoxLayout(self.tool_bar["w"])
        self.tool_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.tool_bar_layout.setSpacing(25)
        self.tool_bar_layout.setAlignment(Qt.AlignCenter)

        # ----- tool Bar Items ----------
        # Normal windows
        windows_stackes_buttons = MW_WINDOW_STAKED_BUTTONS
        for icon,tooltip in windows_stackes_buttons.items():
            btn = QPushButton()
            btn.setIcon(QIcon(os.path.join(ASSETS_ICONS_SVG,f"{icon}.svg")))
            btn.setIconSize(QSize(26, 26))
            btn.setFixedSize(40, 40)
            btn.setToolTip(tooltip)
            btn.setCheckable(True)
            self.tool_bar["stacks"][f"btn_{icon}"] = btn
            self.tool_bar["stacks"][f"btn_{icon}"].clicked.connect(partial(self.cahnge_window,tooltip))
            self.tool_bar_layout.addWidget(btn)
        
        # Pop-Up windows (like the toolbar)
        pop_up_windows_buttons = MW_POPUP_WIDOWS_BUTTONS
        for icon,tooltip in pop_up_windows_buttons.items():
            btn = QPushButton()
            btn.setIcon(QIcon(os.path.join(ASSETS_ICONS_SVG,f"{icon}.svg")))
            btn.setIconSize(QSize(26, 26))
            btn.setFixedSize(40, 40)
            btn.setToolTip(tooltip)
            btn.setCheckable(True)
            self.tool_bar["pop-up"][f"btn_{icon}"] = btn
            self.tool_bar["pop-up"][f"btn_{icon}"].clicked.connect(partial(self.hide_show_popup_window,tooltip))
            self.tool_bar_layout.addWidget(btn)
        
        self.tool_bar["stacks"][f"btn_home"].setChecked(True)


        # ========== Windows =============
        # Staked
        for i,s in self.stcked_windows.items():
            self.stack.addWidget(s)
            s.run()
        self.setCentralWidget(self.stack)

        # Pop-Up
        for u,i in self.popup_windows.items():
            i["m"].hide()
            self.windows.append(i)


    # ======== Slots ============
    # To Change main window
    def cahnge_window(self,w:str):
        self.set_window_t(w)
        self.stack.setCurrentWidget(self.stcked_windows.get(w))
        for i,t in self.tool_bar["stacks"].items():
            self.tool_bar["stacks"][i].setChecked(False)
        if f"btn_{w.lower()}" in self.tool_bar["stacks"]:
            self.tool_bar["stacks"][f"btn_{w.lower()}"].setChecked(True)

    # Show-Run-Hide pupups windows
    def hide_show_popup_window(self,t:str):
        if self.popup_windows.get(t):
            if self.popup_windows[t]["ft?"]:
                self.popup_windows[t]["m"].run()
                self.popup_windows[t]["ft?"] = False
            self.popup_windows[t]["m"].show()
            if f"btn_{t.lower()}" in self.tool_bar["pop-up"]:
                self.tool_bar["pop-up"][f"btn_{t.lower()}"].setChecked(False)

    # ============= pooling =================
    async def update_user_data_on_ui(self):
        try:
            async with aiohttp.ClientSession() as session:
                while True:
                    if self.logged_in is True: 
                        balances = await get_total_balance_in_usdt(USER_BINANCE_INFO["api_key"],USER_BINANCE_INFO["api_secret"],session)
                        

                        self.stcked_windows["Home"].update_user_info(USER_LOCAL_INFO["name"],USER_BINANCE_INFO["user_id"],USER_BINANCE_INFO["account_type"])
                        await UserStream.put({
                            "type": "user_local_info",
                            "event": "user_data_changed",
                            "source": "windows.main.MainWindow.update_user_data_on_ui",
                            "payload": {
                                "user_local_name":USER_LOCAL_INFO["name"],
                                "user_uid":USER_BINANCE_INFO["user_id"],
                                "user_binance_atype":USER_BINANCE_INFO["account_type"]
                            }
                        })

                        if balances != False:
                            total = round(float(balances[0]),2)
                            avilable = round(float(balances[1]),2)
                            frozen = round(float(balances[2]),2)
                            balances_wallet = balances[3]

                            await UserStream.put({
                                "type": "binance_balances",
                                "event": "user_binance_data_changed",
                                "source": "windows.main.MainWindow.update_user_data_on_ui",
                                "payload": {
                                    "total":total,
                                    "avilable":avilable,
                                    "frozen":frozen,
                                    "balances_wallet":balances_wallet
                                }
                            })

                        else:
                            await asyncio.sleep(5)
                            continue
                        await asyncio.sleep(10)
                    else:
                        await asyncio.sleep(10)
        except Exception as e:
            error_(e,"MainWindow.update_user_data_on_ui",str(e))

    # ======== Infrastructure defs ==============

    # On extend window
    def resizeEvent(self, event):
        self.tool_bar["w"].setGeometry(self.tool_bar["geometry"][0],self.height() - 70,self.tool_bar["geometry"][2],self.tool_bar["geometry"][3])
        for u,w in self.popup_windows.items():
            self.popup_windows[u]["m"].setGeometry(self.rect())
        return super().resizeEvent(event)

    # on close window
    def closeEvent(self, event):
        for i in self.windows:
            try:i.close()
            except:pass
        for i in self.async_tasks:
            try:i.cancel()
            except:pass
        AsyncController.window_m(self,"delete")
        event.accept()
        log_("info","Closed main window","MainWindow.closeEvent")
        SystemStream.send({
            "type": "live_sycle",
            "event": "end_of_program",
            "source": "windows.main.MainWindow.closeEvent",
            "payload":{
                "event": "The program finished and closed"
            }
        })
        sys.exit()

    # run the window
    def run(self):
        AsyncController.async_m(asyncio.create_task(self.loggin_logaout_listner()),'add')
        AsyncController.async_m(asyncio.create_task(self.coin_card_clicked()),'add')
        AsyncController.async_m(asyncio.create_task(self.login_button_clicked()),'add')

        AsyncController.async_m(asyncio.create_task(self._on_change_MW_STACKED_WINDOWS()),'add')
        AsyncController.async_m(asyncio.create_task(self._on_change_MW_POPUP_WIDOWS()),'add')
        AsyncController.async_m(asyncio.create_task(self._on_change_MW_WINDOW_STAKED_BUTTONS()),'add')
        AsyncController.async_m(asyncio.create_task(self._on_change_MW_POPUP_WIDOWS_BUTTONS()),'add')

        self.show()

    # ====== events listners ====================================

    # == When login/logout ==
    async def loggin_logaout_listner(self):
        in_sub = UserStream.subscribe("logged_in")
        out_sub = UserStream.subscribe("logged_out")
        task_obj = None

        while True:
            if self.logged_in == False:
                msg = await in_sub.get()
                self.logged_in = True
                self.popup_windows["Login"]["m"].hide()
                await asyncio.sleep(1)
                task_obj = asyncio.create_task(self.update_user_data_on_ui())
                self.async_tasks.append(task_obj)
                AsyncController.async_m(task_obj,'add')
            else:
                msg = await out_sub.get()
                self.logged_in = False
                if task_obj != None:
                    if not task_obj.done():
                        task_obj.cancel()
                        AsyncController.async_m(task_obj,'delete')

    # == when coin-card clicked in markets page ==
    async def coin_card_clicked(self):
        sub = SystemStream.subscribe("coin_clicked")
        while True:
            msg = await sub.get()
            coin = msg["payload"]["coin"]

            try:
                if msg["payload"]["cl_type"] == "coin":

                    wind_name = f"{coin}_COIN"
                    if wind_name in self.stcked_windows.keys():
                        self.cahnge_window(wind_name)
                    else:
                        wid = OneCoin(coin)
                        self.stcked_windows[wind_name] = wid
                        self.stack.addWidget(wid)
                        self.cahnge_window(wind_name)

                elif msg["payload"]["cl_type"] == "pen":
                    self.popup_windows["Charts"]["m"].specific_show(coin=coin)
            except Exception as e:
                error_(e,"MainWindow.coin_card_clicked",str(e))
    
    # == when click login button in any window ==
    async def login_button_clicked(self):
        sub = SystemStream.subscribe("login_clicked")
        while True:
            try:
                await sub.get()
                self.hide_show_popup_window("Login")
            except Exception as e: pass

    # ===== Listners of changes of windows/popup with real time ===

    async def _on_change_MW_STACKED_WINDOWS(self):
        while True:
            await asyncio.sleep(1)
            if self.FIRST_MW_STACKED_WINDOWS != MW_STACKED_WINDOWS:
                differences = set(MW_STACKED_WINDOWS.keys()) - set(self.FIRST_MW_STACKED_WINDOWS.keys())

                for u in list(differences):
                    i = MW_STACKED_WINDOWS[u]
                    self.stcked_windows[u] = i()

            self.FIRST_MW_STACKED_WINDOWS = MW_STACKED_WINDOWS.copy()
    

    async def _on_change_MW_POPUP_WIDOWS(self):
        while True:
            await asyncio.sleep(1)
            if self.FIRST_MW_POPUP_WIDOWS != MW_POPUP_WIDOWS:
                differences = set(MW_POPUP_WIDOWS.keys()) - set(self.FIRST_MW_POPUP_WIDOWS.keys())

                for u in list(differences):
                    i = MW_POPUP_WIDOWS[u]
                    g = i
                    g["m"] = OverlayPopup(self,i["m"]())
                    self.popup_windows[u] = g

            self.FIRST_MW_POPUP_WIDOWS = MW_POPUP_WIDOWS.copy()

    
    async def _on_change_MW_WINDOW_STAKED_BUTTONS(self):
        while True:
            await asyncio.sleep(1)
            if self.FIRST_MW_WINDOW_STAKED_BUTTONS != MW_WINDOW_STAKED_BUTTONS:
                differences = set(MW_WINDOW_STAKED_BUTTONS.keys()) - set(self.FIRST_MW_WINDOW_STAKED_BUTTONS.keys())

                for icon in list(differences):
                    tooltip = MW_WINDOW_STAKED_BUTTONS[icon]
                    btn = QPushButton()
                    btn.setIcon(QIcon(os.path.join(ASSETS_ICONS_SVG,f"{icon}.svg")))
                    btn.setIconSize(QSize(26, 26))
                    btn.setFixedSize(40, 40)
                    btn.setToolTip(tooltip)
                    btn.setCheckable(True)
                    self.tool_bar["stacks"][f"btn_{icon}"] = btn
                    self.tool_bar["stacks"][f"btn_{icon}"].clicked.connect(partial(self.cahnge_window,tooltip))
                    self.tool_bar_layout.addWidget(btn)

                self.tool_bar["geometry"] = [10, self.height() - 70, (len(MW_WINDOW_STAKED_BUTTONS)+len(MW_POPUP_WIDOWS_BUTTONS))*62, 55]
                self.tool_bar["w"].setGeometry(self.tool_bar["geometry"][0],self.height() - 70,self.tool_bar["geometry"][2],self.tool_bar["geometry"][3])
                self.FIRST_MW_WINDOW_STAKED_BUTTONS = MW_WINDOW_STAKED_BUTTONS.copy()

    
    async def _on_change_MW_POPUP_WIDOWS_BUTTONS(self):
        while True:
            await asyncio.sleep(1)
            if self.FIRST_MW_POPUP_WIDOWS_BUTTONS != MW_POPUP_WIDOWS_BUTTONS:
                differences = set(MW_POPUP_WIDOWS_BUTTONS.keys()) - set(self.FIRST_MW_POPUP_WIDOWS_BUTTONS.keys())

                for icon in list(differences):
                    tooltip = MW_POPUP_WIDOWS_BUTTONS[icon]
                    btn = QPushButton()
                    btn.setIcon(QIcon(os.path.join(ASSETS_ICONS_SVG,f"{icon}.svg")))
                    btn.setIconSize(QSize(26, 26))
                    btn.setFixedSize(40, 40)
                    btn.setToolTip(tooltip)
                    btn.setCheckable(True)
                    self.tool_bar["pop-up"][f"btn_{icon}"] = btn
                    self.tool_bar["pop-up"][f"btn_{icon}"].clicked.connect(partial(self.hide_show_popup_window,tooltip))
                    self.tool_bar_layout.addWidget(btn)

                self.tool_bar["geometry"] = [10, self.height() - 70, (len(MW_WINDOW_STAKED_BUTTONS)+len(MW_POPUP_WIDOWS_BUTTONS))*62, 55]
                self.tool_bar["w"].setGeometry(self.tool_bar["geometry"][0],self.height() - 70,self.tool_bar["geometry"][2],self.tool_bar["geometry"][3])
                self.FIRST_MW_POPUP_WIDOWS_BUTTONS = MW_POPUP_WIDOWS_BUTTONS.copy()