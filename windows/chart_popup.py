# ==================================================================
# Import nessary modules
# ==================================================================

# ==libs ==
import os
import asyncio

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

# == local ==
from base.charts import CHARTS_CLASSES,CHARTS
from base.files_folders import ASSETS_ICONS_ICO
from core import AsyncController,log,error,critical_error


# ==================================================================
# Helper classes and functions
# ==================================================================
def critical_error_(ntype:str,source:str=""):
    """
    Specific critical errors function for this file
    """
    critical_error(ntype, f"windows.chart_popup.{source}")

def error_(etype,source:str,msg:str):
    """
    Specific general errors function for this file
    """
    error(etype, f"windows.chart_popup.{source}", msg)

def log_(ltype:str,msg:str,source:str=""):
    """
    Specific log function for this file
    """
    log(ltype,msg, f"windows.chart_popup.{source}")


# ==================================================================
# Main Class
# ==================================================================
class ChowSharts(QWidget):
    clicked = Signal()
    def __init__(self,parent=None):
        super().__init__(parent)
        self.async_tasks = []
        self.spot_symbols = []
        AsyncController.window_m(self,"add")
        

        # ===== Window Settings =====
        self.setWindowTitle("Chart Viewer")
        self.setFixedSize(300, 155)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowIcon(QIcon(os.path.join(ASSETS_ICONS_ICO,"charts.ico")))

        # Values Vars
        self.symbol_value = ''
        self.chart_value = ''
        self.time_frame_value = ''

        # first items when start
        self.FIRST_CHARTS_CLASSES = CHARTS_CLASSES.copy()
        self.FIRST_CHARTS = CHARTS.copy()

        # ===== Create Widgets =======
        self.shart_sellect = {}
        self.time_frame = {}
        self.windows = []
        self.plus_items = []

        # Set Enabled button
        self.shart_sellect['is_correct'] = True
        self.time_frame['is_correct'] = False

        # Set charts vars:
        for name,chart in CHARTS_CLASSES.items():
            try:
                chart.set_chart_vars(self)
            except Exception as e:
                error_(e,"ChowSharts.__init__",f"Chart Name: {name} -> {e}")

        # Chart select
        self.shart_sellect["label"] = QLabel("Shart", self)
        self.shart_sellect["label"].move(10, 21)
        self.shart_sellect["main"] = QComboBox(self)
        self.shart_sellect["main"].setGeometry(87, 13, 200, 35)

        for t, i in CHARTS:
            self.shart_sellect["main"].addItem(t, i)

        # Submit button
        self.submit_button = QPushButton("Add Shart",self)
        self.submit_button.setGeometry(5, 110, 290, 35)

        # Time frame select
        self.time_frame["label"] = QLabel("Time frame", self)
        self.time_frame["label_bottum"] = QLabel("Binance candals intervals", self)
        self.time_frame["label"].move(10, 61)
        self.time_frame["label_bottum"].move(87, 90)

        self.time_frame["main_list"] = QComboBox(self)
        self.time_frame["main_list"].setGeometry(87, 53, 200, 35)
        self.time_frame["main_num"] = QSpinBox(self)
        self.time_frame["main_num"].setGeometry(87, 53, 200, 35)
        
        # set time frame
        self.chart_value = self.shart_sellect["main"].itemData(self.shart_sellect["main"].currentIndex())
        self.plus_items.append(self.time_frame["main_num"])

        self._hide_all()
        self.on_select_chart(self.shart_sellect["main"].currentIndex())

        self.time_frame["main_num"].setRange(1,61)

        # ======= set signals ========
        self.shart_sellect["main"].currentIndexChanged.connect(self.on_select_chart) # On select any shart
        self.time_frame["main_num"].valueChanged.connect(self.on_wright_timefarme_secoundes)
        
        self.submit_button.clicked.connect(self.on_submit)

        AsyncController.async_m(asyncio.create_task(self._on_add_chart()),"add")
        AsyncController.async_m(asyncio.create_task(self._on_add_chart_class()),"add")
        

    # ============ Slots =================

    # On select Chart 
    def on_select_chart(self, index):
        try:
            data = self.shart_sellect["main"].itemData(index)
            self.chart_value = data
            self.time_frame["main_num"].hide()
            self.time_frame["main_list"].hide()
            CHARTS_CLASSES[data].reset_showchart_body(self)
        except Exception as e:
            error_(e,"ChowCharts.on_select_chart",str(e))

    def _e_(self,d):
        self.submit_button.setEnabled(d)

    def _hide_all(self):
        for i in self.plus_items:
            try:i.hide()
            except:pass
    
    def _enable_(self):
        if self.shart_sellect['is_correct'] == False or self.time_frame['is_correct'] == False:
            self._e_(False)
        else:
            self._e_(True)

    # On write time frame by secoundes
    def on_wright_timefarme_secoundes(self,text):
        if text not in [None,0,'',""]:
            self.time_frame_value = int(text)
            self.time_frame['is_correct'] = True
        else:
            self.time_frame['is_correct'] = False
        self._enable_()

    # on push add shart button
    def on_submit(self):   
        CHARTS_CLASSES[self.chart_value].submit_data(self,CHARTS_CLASSES[self.chart_value])

    # ======== Listners of changes ================
    async def _on_add_chart_class(self):
        while True:
            try:
                await asyncio.sleep(1)
                if self.FIRST_CHARTS_CLASSES != CHARTS_CLASSES:
                    differences = set(CHARTS_CLASSES.keys()) - set(self.FIRST_CHARTS_CLASSES.keys())

                    for name in list(differences):
                        chart = CHARTS_CLASSES[name]
                        try:
                            chart.set_chart_vars(self)
                        except Exception as e:
                            error_(e,"ChowSharts._on_add_chart_class",f"Chart Name: {name} -> {e}")

                    self._hide_all()
                    self.on_select_chart(self.shart_sellect["main"].currentIndex())
                    self.FIRST_CHARTS_CLASSES = CHARTS_CLASSES.copy()
            except Exception as e:
                error_(e,"ChowSharts._on_add_chart_class",str(e))

    async def _on_add_chart(self):
        while True:
            try:
                await asyncio.sleep(1)
                if self.FIRST_CHARTS != CHARTS:
                    differences = set(CHARTS) - set(self.FIRST_CHARTS)

                    for t, i in list(differences):
                        self.shart_sellect["main"].addItem(t, i)
                        
                    self._hide_all()
                    self.on_select_chart(self.shart_sellect["main"].currentIndex())
                    self.FIRST_CHARTS = CHARTS.copy()
            except Exception as e:
                error_(e,"ChowSharts._on_add_chart",str(e))

    # ======== Infrastructure defs ==============

    # On click in widget
    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

    # on close window
    def closeEvent(self, event):
        for i in self.windows:
            try:i.close()
            except:pass
        for i in self.async_tasks:
            i.cancel()
        event.accept()

    def run(self):
        self.show()

    def specific_show(self,coin):
        self.symbol_value = str(coin)