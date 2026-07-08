# ==================================================================
# Import nessary modules
# ==================================================================

# ==libs ==
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import Qt
from PySide2.QtCore import Qt,QObject,Slot
from PySide2.QtWebChannel import QWebChannel
import asyncio

# == local ==
from core import AsyncController,log,error,critical_error,SystemStream,UserStream
from Styles.css import CSS


# ==================================================================
# Helper classes and functions
# ==================================================================
def critical_error_(ntype:str,source:str=""):
    """
    Specific critical errors function for this file
    """
    critical_error(ntype, f"windows.tool_bar.home{source}")

def error_(etype,source:str,msg:str):
    """
    Specific general errors function for this file
    """
    error(etype, f"windows.tool_bar.home{source}", msg)

def log_(ltype:str,msg:str,source:str=""):
    """
    Specific log function for this file
    """
    log(ltype,msg, f"windows.tool_bar.home{source}")

class Backend(QObject):
    def __init__(self):
        super().__init__()

    @Slot()
    def on_login_clicked(self):
        SystemStream.send({
            "type": "window_event",
            "event": "login_clicked",
            "source": "windows.tool_bar.home.Backend.on_login_clicked",
            "payload":{
                "event":"The login button clicked, open login page"
            }
        })

# ==================================================================
# Vars
# ==================================================================

HTML = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Home page</title>
        <style> """ + CSS["MAIN"] + """</style>
        <script>
            var backend;
            new QWebChannel(qt.webChannelTransport, function (channel) {
                backend = channel.objects.backend;
            });
        </script>
    </head>
    <body>

    <header>
        <div>
            <h2 id="user-name">Account Name </h2>
            <p><b>Binance UID</b>: <span id="user-binance-uid">-----</span></p>
            <p><b>Account Type</b>: <span id="user-accont-type">------</span></p>
        </div>
        <p id="login-btn-space"><button class="login-btn" onclick="backend.on_login_clicked()">Login</button></p>
    </header>

    <div class="container">

        <!-- Big Balance -->
        <div class="card balance-card">
            <h2>Total Balance</h2>
            <div class="total"><span id="total-balance__main-card">----.--</span> USDT</div>
            <span class="sub"> <b>Availabel:</b> <span id="avilabel-balance__main-card">----.--</span> | <b>Frozen:</b> <span id="frozen-balance__main-card">----.--</span> </span>
        </div>

        <!--
        <div class="card">
            <h2>Profit & Loss</h2>
            <p>Daily PnL: <span class="profit" id="daily-pnl">---- USDT (---%) ↑</span></p>
            <p>Weekly PnL: <span class="loss" id="weekly-pnl">---- USDT (---%) ↓</span></p>
            <p>Monthly PnL: <span class="profit" id="monthly-pnl">---- USDT (---%) ↑</span></p>
        </div>

        <div class="card">
            <h2>Open Orders</h2>
            <table>
                <tr>
                    <th>Time ⏱</th>
                    <th>Coin</th>
                    <th>Stop Loss</th>
                    <th>Take Profit</th>
                    <th>PnL</th>
                    <th>Status</th>
                    <th>Size</th>
                </tr>


                <tr>
                    <td>11:00</td>
                    <td>ETH/USDT</td>
                    <td>1,750</td>
                    <td>1,900</td>
                    <td class="loss">-45 USDT</td>
                    <td>Pending</td>
                    <td>2</td>
                </tr>

            </table>
        </div>

    
        <div class="card">
            <h2>Recent Trades</h2>
            <table id="recent-trades">
                <tr>
                    <th>Time ⏱</th>
                    <th>Coin</th>
                    <th>Stop Loss</th>
                    <th>Take Profit</th>
                    <th>PnL</th>
                    <th>Size</th>
                </tr>


                <tr>
                    <td>10:30</td>
                    <td>BTC/USDT</td>
                    <td>27,800</td>
                    <td>29,500</td>
                    <td class="profit">+120 USDT</td>
                    <td>0.1</td>
                </tr>

            </table>
        </div>

    </div>
    <script>
        document.getElementById("recent-trades").insertAdjacentHTML("beforeend", `
      <tr>
        <td>12:00</td>
        <td>BNB/USDT</td>
        <td>1,750</td>
        <td>1,900</td>
        <td class="loss">-45 USDT</td>
        <td>3</td>
      </tr>
    `);
    </script>
    -->

    </body>
    </html>
    """

class Home(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.async_tasks = []
        self.windows = []
        self.uploaded_ok = False
        self.logged_in = False
        log_("info","Home Page loaded and started","Home.__init__")
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

    def update_user_info(self,name="-----",uid="-----",type_="-----"):
        if self.uploaded_ok:
            self.page().runJavaScript(f"""
                document.getElementById('user-name').innerHTML = "{name}";
                document.getElementById('user-binance-uid').innerHTML = "{uid}";
                document.getElementById('user-accont-type').innerHTML = "{type_}";
            """)

    # ======== Events listners ===========

    # == When login/logout ==
    async def loggin_logaout_listner(self):
        in_sub = UserStream.subscribe("logged_in")
        out_sub = UserStream.subscribe("logged_out")

        while True:
            if self.logged_in == False:
                msg = await in_sub.get()
                self.page().runJavaScript(f" document.getElementById('login-btn-space').innerHTML = `Home Page` ")
                self.logged_in = True
            else:
                msg = await out_sub.get()
                self.page().runJavaScript(f' document.getElementById("login-btn-space").innerHTML = `<button class="login-btn" onclick="backend.on_login_clicked()">Login</button>` ')
                self.update_bilances()
                self.update_user_info()
                self.logged_in = False

    # == When binance data changed ==
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

            

    # ======== Infrastructure defs ==============
    # on close window
    def closeEvent(self, event):
        for i in self.windows:
            try:i.close()
            except:pass
        for i in self.async_tasks:
            i.cancel()
        AsyncController.window_m(self,"delete")
        event.accept()

    # Start all functions and show window
    def run(self):
        AsyncController.async_m(asyncio.create_task(self.loggin_logaout_listner()))
        AsyncController.async_m(asyncio.create_task(self.change_bilances_listner()))
        self.show()