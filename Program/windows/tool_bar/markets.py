# ==================================================================
# Import nessary modules
# ==================================================================

# ==libs ==
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtCore import Qt,QObject,Slot

# == local ==
from core import AsyncController,log,error,critical_error,SystemStream
from Styles.css import CSS


# ==================================================================
# Helper classes and functions
# ==================================================================
class Backend(QObject):
    def __init__(self):
        super().__init__()

    @Slot(str)
    def on_coin_clicked(self,coin:str):
        SystemStream.send({
            "type": "window_event",
            "event": "coin_clicked",
            "source": "windows.tool_bar.markets.Backend.on_coin_clicked",
            "payload":{
                "cl_type": "coin",
                "coin":coin,
                "event": f"Coin {coin} bar clicked in markets page (need to open page of one coin)",
                "headen":True
            }
        })

    @Slot(str)
    def on_pen_clicked(self,coin:str):
        SystemStream.send({
            "type": "window_event",
            "event": "coin_clicked",
            "source": "windows.tool_bar.markets.Backend.on_pen_clicked",
            "payload":{
                "cl_type": "pen",
                "coin":coin,
                "event": f"Pen of coin {coin} bar clicked in markets page (need to open chow_charts popup window)",
                "headen":True
            }
        })

def critical_error_(ntype:str,source:str=""):
    """
    Specific critical errors function for this file
    """
    critical_error(ntype, f"windows.tool_bar.markets{source}")

def error_(etype,source:str,msg:str):
    """
    Specific general errors function for this file
    """
    error(etype, f"windows.tool_bar.markets{source}", msg)

def log_(ltype:str,msg:str,source:str=""):
    """
    Specific log function for this file
    """
    log(ltype,msg, f"windows.tool_bar.markets{source}")

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
<title>Coins</title>

<style>
"""+ CSS["MAIN"] +"""
</style>
<script>
    var backend;
    new QWebChannel(qt.webChannelTransport, function (channel) {
        backend = channel.objects.backend;
    });
</script>
</head>

<body>

<header>

<h2>Markets</h2>
<p>All cryptocurrency markets on Binance</p>

<script>

/* =================================
   FUNCTIONS REQUESTED
================================= */

function pen_clicked(coin){
    backend.on_pen_clicked(coin)
}

function coin_clicked(coin){
    backend.on_coin_clicked(coin)
}

</script>

</header>


<div class="container">

<div class="search-bar">
<input id="search" placeholder="Search coin...">
</div>

<div id="coins" class="coins-grid"></div>

</div>



<script>

const coins_container = document.getElementById("coins")
const search_input = document.getElementById("search")

let coins = {}
let coin_list = []

/* ============================
   GET BINANCE SYMBOLS
============================ */

async function load_symbols(){

    const res = await fetch("https://api.binance.com/api/v3/exchangeInfo")
    const data = await res.json()

    const symbols = data.symbols

    symbols.forEach(s=>{

        if(s.symbol.endsWith("USDT")){

            const coin = s.symbol.replace("USDT","")

            coin_list.push({
                symbol:s.symbol,
                coin:coin
            })

        }

    })

    render_coins()

}

/* ============================
   RENDER COINS
============================ */

function render_coins(filter=""){

    coins_container.innerHTML=""

    coin_list.forEach(item=>{

        if(filter && !item.coin.toLowerCase().includes(filter.toLowerCase()))
            return

        const card=document.createElement("div")
        card.className="coin-card"
        card.dataset.symbol=item.symbol

        card.onclick=()=>{
            coin_clicked(item.coin)
        }

        const price=coins[item.symbol] || "..."

        card.innerHTML=`

        <div class="pen">✏</div>

        <div class="coin-name">${item.coin}</div>
        <div class="coin-price" id="price_${item.symbol}">${price}</div>

        `

        const pen=card.querySelector(".pen")

        pen.onclick=(e)=>{
            e.stopPropagation()
            pen_clicked(item.coin)
        }

        coins_container.appendChild(card)

    })

}

/* ============================
   SEARCH
============================ */

search_input.addEventListener("input",()=>{

    render_coins(search_input.value)

})


/* ============================
   WEBSOCKET REALTIME PRICES
============================ */

function start_ws(){

    const ws=new WebSocket("wss://stream.binance.com:9443/ws/!miniTicker@arr")

    ws.onmessage=(event)=>{

        const data=JSON.parse(event.data)

        data.forEach(ticker=>{

            const symbol=ticker.s

            if(symbol.endsWith("USDT")){

                coins[symbol]=parseFloat(ticker.c).toFixed(4)

                const el=document.getElementById("price_"+symbol)

                if(el){
                    el.innerText=coins[symbol]
                }

            }

        })

    }

}

/* ============================
   START
============================ */

load_symbols()
start_ws()

</script>


</body>
</html>
"""

class Markets(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.async_tasks = []
        self.windows = []
        self.uploaded_ok = False
        self.channel = QWebChannel(self)
        self.backend = Backend()
        self.channel.registerObject("backend",self.backend)
        self.page().setWebChannel(self.channel)
        log_("info","Markets Page loaded and started","Markets.__init__")
        AsyncController.window_m(self,"add")

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
        self.show()