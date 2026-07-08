# ==================================================================
# Import nessary modules
# ==================================================================

# ==libs ==
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import Qt,QObject,Slot
from PySide2.QtWebChannel import QWebChannel
import asyncio

# == local ==
from core import AsyncController,log,error,critical_error,UserStream,SystemStream
from Styles.css import CSS
from base.utils import STABLECOINS_USD


# ==================================================================
# Helper classes and functions
# ==================================================================
def critical_error_(ntype:str,source:str=""):
    """
    Specific critical errors function for this file
    """
    critical_error(ntype, f"windows.tool_bar.wallet{source}")

def error_(etype,source:str,msg:str):
    """
    Specific general errors function for this file
    """
    error(etype, f"windows.tool_bar.wallet{source}", msg)

def log_(ltype:str,msg:str,source:str=""):
    """
    Specific log function for this file
    """
    log(ltype,msg, f"windows.tool_bar.wallet{source}")

class Backend(QObject):
    def __init__(self):
        super().__init__()

    @Slot()
    def on_login_clicked(self):
        SystemStream.send({
            "type": "window_event",
            "event": "login_clicked",
            "source": "windows.tool_bar.wallet.Backend.on_login_clicked",
            "payload":{
                "event":"The login button clicked, open login page"
            }
        })

# ==================================================================
# Vars
# ==================================================================

HTML = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Wallet</title>
        <style>""" + CSS["MAIN"] + """</style>
        <script>
            var backend;
            new QWebChannel(qt.webChannelTransport, function (channel) {
                backend = channel.objects.backend;
            });
        </script>
    </head>
    <body>
        <!-- Header -->
        <header>
            <h2>Wallet</h2>
            <p id="login-btn-space"><button class="login-btn" onclick="backend.on_login_clicked()">Login</button></p>
            <!-- Your crypto overview -->
        </header>

        <!-- Main Container -->
        <div class="container">

            <!-- Balance Card -->
            <div class="balance-card">
                <h3>Total Balance</h3>
                <div class="total"><span id="total-balance__main-card">----.--</span> USDT</div>
                <span class="sub"> <b>Availabel:</b> <span id="avilabel-balance__main-card">----.--</span> | <b>Frozen:</b> <span id="frozen-balance__main-card">----.--</span> </span>
            </div>

            <!-- Wallet Cards -->
            <div class="card">
                <h2>Assets</h2>
                <div class="pairs-list" id="pairs-list__wallet" > 
                </div>
            </div>


            <!--
            <div class="card">
                <h2>Recent Trades</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Pair</th>
                            <th>Type</th>
                            <th>Amount</th>
                            <th>Price</th>
                            <th>Profit/Loss</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>BTC/USDT</td>
                            <td>Buy</td>
                            <td>0.1 BTC</td>
                            <td>$28,000</td>
                            <td class="profit">+$500</td>
                        </tr>
                        <tr>
                            <td>ETH/USDT</td>
                            <td>Sell</td>
                            <td>1 ETH</td>
                            <td>$1,850</td>
                            <td class="loss">-$50</td>
                        </tr>
                        <tr>
                            <td>BNB/USDT</td>
                            <td>Buy</td>
                            <td>2 BNB</td>
                            <td>$320</td>
                            <td class="profit">+$30</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

    -->
    </body>
    </html>
"""

class Wallet(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.async_tasks = []
        self.logged_in = False
        log_("info","Wallet Page loaded and started","Wallet.__init__")
        AsyncController.window_m(self,"add")

        self.channel = QWebChannel(self)
        self.backend = Backend()
        self.channel.registerObject("backend",self.backend)
        self.page().setWebChannel(self.channel)

        self.setHtml(HTML)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.loadFinished.connect(lambda ok: self.load_finished())
        self.loadFinished.connect(lambda ok: self.run())

    def load_finished(self): self.uploaded_ok = True

    # ==== Click-right-list =====
    def show_context_menu(self, pos):
        menu = QMenu(self)

        reload_action = QAction("Reload", self)
        reload_action.triggered.connect(self.reload)

        back_action = QAction("Back", self)
        back_action.triggered.connect(self.back)

        forward_action = QAction("Forward", self)
        forward_action.triggered.connect(self.forward)

        menu.addAction(back_action)
        menu.addAction(forward_action)
        menu.addSeparator()
        menu.addAction(reload_action)

        menu.exec_(self.mapToGlobal(pos))

    def update_bilances(self,total="----.--",avilable="----.--",frozen="----.--"):
        if self.uploaded_ok:
            self.page().runJavaScript(f"""
                document.getElementById('total-balance__main-card').innerHTML = "{total}";
                document.getElementById('avilabel-balance__main-card').innerHTML = "{avilable}";
                document.getElementById('frozen-balance__main-card').innerHTML = "{frozen}";
            """)

    def _update_wallet(self,balances):
        list_html = ''
        for asset in balances:
            asset_name:str = asset["asset"]
            available = float(asset["free"])
            frozen = float(asset["locked"])
            if available + frozen == 0: continue
            pair_html = f""" <div class="pair" style="margin-top:5px;margin-bottom:5px;">
                    <div class="left">
                        <img src="https://api.elbstream.com/logos/crypto/{asset_name.lower()}" alt="{asset_name.upper()}" class="icon">
                        <span class="symbol">&nbsp;{asset_name.upper()}</span>
                    </div>
                    <div class="middle">
                        <span class="price">{round(available + frozen,2) if asset_name.upper() in STABLECOINS_USD else available + frozen} {asset_name.upper()}</span>
                    </div>
                    <div class="balances">
                        <span class="available">{available}</span>
                        <span class="frozen">{frozen}</span>
                    </div>
                </div> 
            """
            list_html += pair_html
        self.page().runJavaScript(f""" document.getElementById('pairs-list__wallet').innerHTML = `{list_html}` """)

    def update_wallet(self,balances=[]):
        if self.uploaded_ok:
            self._update_wallet(balances)

    # === obj listners ===
    async def change_bilances_listner(self):
        sub = UserStream.subscribe("user_binance_data_changed")
        while True:
            msg = await sub.get()
            data = msg.get("payload")
            self.update_bilances(
                total=data["total"],
                avilable=data["avilable"],
                frozen=data["frozen"]
            )
            self.update_wallet(data["balances_wallet"])

    # == When login/logout ==
    async def loggin_logaout_listner(self):
        in_sub = UserStream.subscribe("logged_in")
        out_sub = UserStream.subscribe("logged_out")

        while True:
            if self.logged_in == False:
                msg = await in_sub.get()
                self.page().runJavaScript(f" document.getElementById('login-btn-space').innerHTML = `Your crypto overview` ")
                self.logged_in = True
            else:
                msg = await out_sub.get()
                self.page().runJavaScript(f' document.getElementById("login-btn-space").innerHTML = `<button class="login-btn" onclick="backend.on_login_clicked()">Login</button>` ')
                self.update_wallet()
                self.update_bilances()
                self.logged_in = False
                

    # ======== Infrastructure defs ==============
    # on close window
    def closeEvent(self, event):
        for i in self.windows:
            try:i.close()
            except:pass
        for i in self.async_tasks:
            i.cancel()
        event.accept()
    # Start all functions and show window
    def run(self):
        AsyncController.async_m(asyncio.create_task(self.change_bilances_listner()))
        AsyncController.async_m(asyncio.create_task(self.loggin_logaout_listner()))
        self.show()