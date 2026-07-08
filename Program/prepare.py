# ==================================================================
# initialyze env
# ==================================================================

import os

from Program.charts import candlestick_chart
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox --disable-gpu --disable-software-rasterizer"
os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
os.environ["PYQTGRAPH_QT_LIB"] = "PySide2"

# ==================================================================
# Import nessary modules
# ==================================================================

# == libs ==
import asyncio
import logging
from threading import Thread

# == local ==
from Styles import mods,icons
import core
import base
import API
from core import folders
from base import charts,tool_bar
from charts import order_book
from windows.tool_bar import home,wallet,markets
from core import SystemStream

# ==================================================================
# Vars
# ==================================================================
listners_objs = [core,API]

# ==================================================================
# Executation
# ==================================================================

# == start all listners ==
for obj in listners_objs:
    for i in obj.listeners: 
        asyncio.create_task(i())
logging.debug("All listners are ready")

# == Charts classes ==
charts.CHARTS_CLASSES["candals_shart"] = candlestick_chart.SimpleCandelsChart
charts.CHARTS_CLASSES["order_book"] = order_book.OrderBook

# == Tool bar classes ==
tool_bar.MW_STACKED_WINDOWS["Home"] = home.Home
tool_bar.MW_STACKED_WINDOWS["Wallet"] = wallet.Wallet
tool_bar.MW_STACKED_WINDOWS["Markets"] = markets.Markets

# == popup windows ==
from windows.chart_popup import ChowSharts
from user.window import AuthMain
tool_bar.MW_POPUP_WIDOWS["Charts"] = {"m":ChowSharts,"ft?":True}
tool_bar.MW_POPUP_WIDOWS["Login"] = {"m":AuthMain,"ft?":True}

logging.debug("Tool bar is ready")

# == Start system message ==
SystemStream.send({
    "type": "live_sycle",
    "event": "start_of_program",
    "source": "prepare",
    "payload":{
        "event": "The program Started"
    }
})