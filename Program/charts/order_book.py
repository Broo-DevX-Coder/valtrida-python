# ==================================================================
# Import nessary modules
# ==================================================================

# == libs ==
import time
import asyncio
import aiohttp
import asyncio
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import *

# == local ==
from Styles.qss import QSS
from API import CHOISED_SYMBOLS_CLASS
from core import AsyncController,log


# ==================================================================
# Helper classes and functions
# ==================================================================

def log_(ltype:str,msg:str,source:str=""):
    """
    Specific log function for this file
    """
    log(ltype,msg, f"charts.order_book.{source}")

# ==================================================================
# Main classes
# ==================================================================

class OrderBookSideWindow(QWidget):
    """Single-side Order Book (Bids or Asks) like Binance"""
    closed = QtCore.Signal(object)

    def __init__(self, symbol: str, price_decimals: int, vol_unit: str, side: str):
        super().__init__()
        self.setWindowTitle(f"{symbol} Order Book - {side.capitalize()}")
        self.resize(400, 600)
        self.setFixedWidth(400)
        self.setStyleSheet(QSS["BINANCE"])

        self.symbol = symbol
        self.PRICE_DECIMALS = price_decimals
        self.VOL_UNIT = vol_unit
        self.side = side  

        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Price", f"Quantity ({vol_unit})", "Quantity (USD)"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("""
            QTableWidget { background-color: black; color: white; gridline-color: #333; }
            QHeaderView::section { background-color: #111; color: #ccc; }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

    def update_side(self, levels: list):
        """
        Update the table with one side of the order book.
        levels: list of (price, qty)
        """
        self.table.setRowCount(len(levels))

        if self.side == "asks":
            # asks => sorted ascending (lowest ask on top)
            levels = sorted(levels, key=lambda x: x[0])
            color = "red"
        else:
            # bids => sorted descending (highest bid on top)
            levels = sorted(levels, key=lambda x: -x[0])
            color = "lime"

        for i, (p, q) in enumerate(levels):
            self._set_row(i, p, q, p*q, color=color)

    def _set_row(self, row, price, qty, cum, color="white"):
        """Helper to insert one row into table"""
        price_item = QTableWidgetItem(f"{price:.{self.PRICE_DECIMALS}f}")
        qty_item = QTableWidgetItem(f"{qty:.4f}")
        total_item = QTableWidgetItem(f"{cum:.4f}")

        for item in (price_item, qty_item, total_item):
            item.setTextAlignment(QtCore.Qt.AlignCenter)

        # color price cell
        price_item.setForeground(QtGui.QColor(color))

        self.table.setItem(row, 0, price_item)
        self.table.setItem(row, 1, qty_item)
        self.table.setItem(row, 2, total_item)

    def closeEvent(self, event):
        try:
            self.closed.emit(self)
        except Exception:
            pass
        AsyncController.window_m(self,"delete")
        super().closeEvent(event)

    def run(self):
        self.show()

class OrderBook():
    """Custom chart widget for visualizing Binance order book depth."""

    def __init__(self,time_frame: int = 1,symbol: str = "SOLUSDT"):
        self.async_tasks = []
        self.opened_windows = []
        log_('info',f'Start Orderbook for {symbol}','OrderBook.__init__')

        # Set Vars
        self.TIME_MS: int = int(time_frame)*1000
        self.SYMBOL = symbol
        self.SCATTER_SIZE = 10
        self.PRICE_DICIAMELS = 2
        self.ORDERBOOK_LIMIT = 3000
        self.symbol_obj = CHOISED_SYMBOLS_CLASS(self.SYMBOL)

        self.rest_session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(20))
        AsyncController.window_m(self,'add')

    def time_n(self):
        """Return current time in milliseconds."""
        return time.time() * 1000

    async def _polling_update(self):
        await self.symbol_obj.initialize()
        await self.symbol_obj.orderbook_initialyze(limit=self.ORDERBOOK_LIMIT)
        while True:
            ob = await self.symbol_obj.recv_orderbook(self.TIME_MS/1000)
            for win in self.opened_windows:
                if win.side == "bids": win.update_side(list(ob["bids"].items()))
                if win.side ==  "asks": win.update_side(list(ob["asks"].items()))

    # ======== Infrastructure defs ==============

    # Reset ChowCharts When the olugin seted
    @staticmethod
    def reset_showchart_body(parent):
        parent.on_wright_timefarme_secoundes(parent.time_frame["main_num"].value())
        parent._hide_all()
        parent.setFixedSize(300, 155)
        parent.time_frame["label"].setText("Time delta")
        parent.submit_button.setGeometry(5, 110, 290, 35)
        
        parent.time_frame["main_num"].show()
        parent.time_frame["label_bottum"].setText("Secondes unit")
        parent.time_frame['is_correct'] = False if parent.time_frame["main_num"].value() in [None,0,'',""] else True

    # Creat the shart wen Add Button in show shart pushed
    @staticmethod
    def submit_data(parent,chart):
        parent.time_frame_value = parent.time_frame["main_num"].value()
        w = chart(symbol=parent.symbol_value,time_frame=parent.time_frame_value)
        parent.windows.append(w)
        w.run()

    @staticmethod
    def set_chart_vars(parent):
        pass

    # ======================================================

    def close(self):
        # Non-blocking request to close async resources
        try:
            asyncio.create_task(self.close_async())
            for win in self.opened_windows:
                win.close()
        except (RuntimeError,RuntimeWarning):
            try:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.close_async())
            except Exception:
                pass

    async def colse_session(self):
        await self.rest_session.close()

    def _on_child_closed(self, win):
        """Called when a child OrderBookSideWindow is closed."""
        try:
            if win in self.opened_windows:
                self.opened_windows.remove(win)
        except Exception:
            pass

        if len(self.opened_windows) == 0:
            # schedule the async close (don't await here)
            try:
                asyncio.create_task(self.close_async())
            except Exception:
                # fallback to call close() which schedules close_async
                self.close()

    async def close_async(self):
        """Proper async shutdown: close rest session, cancel tasks, close windows."""
        # prevent re-entrance
        if getattr(self, "_closing", False):
            return
        self._closing = True

        # cancel background tasks gracefully
        for t in list(self.async_tasks):
            try:
                t.cancel()
            except Exception:
                pass

        # allow tasks to cancel
        await asyncio.sleep(0)

        # close rest session
        try:
            await self.rest_session.close()
        except Exception:
            pass

        # close any remaining windows (safe)
        for win in list(self.opened_windows):
            try:
                win.close()
            except Exception:
                pass
        self.opened_windows.clear()

        log_('info',f"Order Book for {self.SYMBOL.upper()} Closed","OrderBook.close_async")


    # Start chart
    def run(self):
        """Run background update tasks."""
        bids_win = OrderBookSideWindow(self.SYMBOL.upper(), 2, self.SYMBOL.upper().replace("USDT",""), side="bids")
        asks_win = OrderBookSideWindow(self.SYMBOL.upper(), 2, self.SYMBOL.upper().replace("USDT",""), side="asks")
        
        for win in (asks_win, bids_win):
            win.closed.connect(self._on_child_closed)
            self.opened_windows.append(win)

        task3 = asyncio.create_task(self._polling_update());task3
        self.async_tasks.append(task3)

        for win in self.opened_windows:
            try:win.run()
            except Exception: pass


# ==================================================================
# Run if this file not imported
# ==================================================================

if __name__ == "__main__":
    from core.async_controller import CRITICAL_STOP
    import sys
    import qasync


    app = QApplication(sys.argv)
    loop = qasync.QEventLoop()

    async def main():
        obj__ = OrderBook()
        obj__.run()
        while True:
            await asyncio.sleep(1000)

    try:
        with loop:
            loop.run_until_complete(main())
    except (RuntimeError, KeyboardInterrupt):
        pass