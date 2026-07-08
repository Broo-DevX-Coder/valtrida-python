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
    def on_pen_clicked(self,coin:str):
        SystemStream.send({
            "type": "window_event",
            "event": "coin_clicked",
            "source": "windows.coin.Backend.on_pen_clicked",
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
    critical_error(ntype, f"windows.coin{source}")

def error_(etype,source:str,msg:str):
    """
    Specific general errors function for this file
    """
    error(etype, f"windows.coin{source}", msg)

def log_(ltype:str,msg:str,source:str=""):
    """
    Specific log function for this file
    """
    log(ltype,msg, f"windows.coin{source}")

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

<title>Coin Page</title>
<script>
    const coin = "<Here-Coin-Symbol>"
</script>

<style>

""" + CSS["MAIN"] + """

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

<div class="coin-header">

<img id="coin-icon" class="coin-icon">

<div>
<h2 id="coin-title">BTC</h2>
<p>Market Overview</p>
</div>

</div>

<button class="pen-btn" onclick="pen_clicked()">✏</button>

</header>


<div class="container">

<!-- PRICE CARD -->

<div class="balance-card">

<h3>Current Price</h3>

<div class="total" id="price">----</div>

<span class="sub">
24h Change: <span id="change">---</span>
</span>

</div>


<!-- STATS -->

<div class="card">

<h2>Market Stats</h2>

<div class="trade-info">

<div class="info-box">
<h3>24h High</h3>
<p id="high">---</p>
</div>

<div class="info-box">
<h3>24h Low</h3>
<p id="low">---</p>
</div>

<div class="info-box">
<h3>Volume</h3>
<p id="volume">---</p>
</div>

<div class="info-box">
<h3>Symbol</h3>
<p id="symbol">---</p>
</div>

</div>

</div>


<!-- CHART -->

<div class="card">

<h2>Price Chart</h2>

<canvas id="chart" height="120"></canvas>

</div>


</div>


<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>

const symbol = coin + "USDT"

function formatPrice(price){

price = Number(price)

if (price >= 1000) return price.toFixed(2)
if (price >= 1) return price.toFixed(4)
if (price >= 0.01) return price.toFixed(6)
if (price >= 0.0001) return price.toFixed(8)

return price.toPrecision(4)

}

/* ---------- SET ICON ---------- */

document.getElementById("coin-icon").src =
`https://cdn.jsdelivr.net/gh/vadimmalykhin/binance-icons/crypto/${coin.toLowerCase()}.svg`

document.getElementById("coin-title").innerText = coin
document.getElementById("symbol").innerText = symbol


/* ---------- PEN CLICK ---------- */

function pen_clicked(){
    backend.on_pen_clicked(coin)
}


/* ---------- MARKET DATA ---------- */

async function load_market(){

const res = await fetch(
`https://api.binance.com/api/v3/ticker/24hr?symbol=${symbol}`
)

const data = await res.json()

document.getElementById("price").innerText =
formatPrice(parseFloat(data.lastPrice))

const change = parseFloat(data.priceChangePercent)

const changeEl = document.getElementById("change")

changeEl.innerText = formatPrice(change) + "%"

if(change >= 0){
changeEl.className="profit"
}else{
changeEl.className="loss"
}

document.getElementById("high").innerText =
formatPrice(parseFloat(data.highPrice))

document.getElementById("low").innerText =
formatPrice(parseFloat(data.lowPrice))

document.getElementById("volume").innerText =
formatPrice(parseFloat(data.volume))

}


/* ---------- CHART ---------- */

async function load_chart(){

const res = await fetch(
`https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=1h&limit=60`
)

const data = await res.json()

const labels = data.map(c=>{
const d=new Date(c[0])
return d.getHours()+":00"
})

const prices = data.map(c=>parseFloat(c[4]))

new Chart(document.getElementById("chart"),{

type:"line",

data:{
labels:labels,
datasets:[{
data:prices,
borderColor:"#4aa96c",
borderWidth:2,
fill:false
}]
},

options:{
plugins:{legend:{display:false}}
}

})

}


/* ---------- REALTIME PRICE ---------- */

function realtime(){

const ws = new WebSocket(
`wss://stream.binance.com:9443/ws/${symbol.toLowerCase()}@miniTicker`
)

ws.onmessage = (event)=>{

const data = JSON.parse(event.data)

const price = parseFloat(data.c)
const open = parseFloat(data.o)

/* ---------- PRICE ---------- */

document.getElementById("price").innerText = formatPrice(price)

/* ---------- CHANGE ---------- */

const change = ((price - open) / open) * 100

const changeEl = document.getElementById("change")

changeEl.innerText = formatPrice(change) + "%"

if(change >= 0){
changeEl.className = "profit"
}else{
changeEl.className = "loss"
}

/* ---------- VOLUME ---------- */

document.getElementById("volume").innerText =
formatPrice(parseFloat(data.v))

/* ---------- HIGH LOW ---------- */

document.getElementById("high").innerText =
formatPrice(parseFloat(data.h))

document.getElementById("low").innerText =
formatPrice(parseFloat(data.l))

}

}


/* ---------- INIT ---------- */

load_market()
load_chart()
realtime()

</script>

</body>
</html>

"""

class OneCoin(QWebEngineView):
    def __init__(self,coin:str,parent=None):
        super().__init__(parent)
        self.coin=coin
        self.async_tasks = []
        self.windows = []
        self.uploaded_ok = False
        self.channel = QWebChannel(self)
        self.backend = Backend()
        self.channel.registerObject("backend",self.backend)
        self.page().setWebChannel(self.channel)
        log_("info",f"Coin Page loaded and started for {coin}","Markets.__init__")
        AsyncController.window_m(self,"add")

        self.setHtml(HTML.replace("<Here-Coin-Symbol>",coin))

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