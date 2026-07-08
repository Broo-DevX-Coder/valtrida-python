# ==================================================================
# Import nessary modules
# ==================================================================

# == libs ==
import asyncio
import aiohttp
from uniquant.Platforms import Binance

# == local ==
from base.utils import QueueStream,STABLECOINS_USD,uuid_gen
from core import AsyncController,critical_error,log,error

# ==================================================================
# Vars
# ==================================================================
ALL_SYMBOLS = [] # List of all geted symbols 
ALL_USDT_SYMBOLS = [] # List of all geted symbols that end with USDT
ALL_COINS = [] # List of all coins that we want to get data for (extracted from symbols)

PLATFORMS_OBJS = { # Dictionary to store the API classes for each platform, allowing for easy access and management of different platforms' APIs.
    "Binance":{
        "PublicSymbols": Binance.Public.PublicSymbols,
        "OneSymbole": Binance.Public.OneSymbole
    }
}

SYMBOLS_DATA = {}
"""
    'Binance':{
        "symbol": {
            "base_asset":str(),
            "quote_asset":str(),
            "status":{
                OB:"open"/"closed",
                TRADES:"open"/"closed"
            },
            "operations_queue":{
                OB:"open"/"closed",
                TRADES:"open"/"closed"
            },
            "one_symbol_obj":OneSymbole(),
            "errors_stream":QueueStream(),
            "orderbook": {"asks":{}, "bids":{}},
            "trades_stream":QueueStream()
        }
    }
"""

# ==================================================================
# Nedded Classes and functions
# ==================================================================

# Critical connection errors stream (it redirected to the main ErrorsStream in async_controller.py to be handled and displayed in the UI)
Connection_errors = QueueStream()

# Rediresct the critical connection errors to the main ErrorsStream in async_controller.py
async def redirect_connection_errors():
    sub = Connection_errors.subscribe()
    while True:
        msg = await sub.get()
        sub.task_done()
        source = msg["source"]
        e_type = msg["type"]
        if e_type == "CONNECTION_429" or e_type == "CONNECTION_418" or e_type == "CONNECTION_403" or e_type == "CONNECTION_0":
            ntype = e_type.replace("CONNECTION_","")
            critical_error(ntype,f"api.uniquant.{source}")
        else:
            error(e_type,f"api.uniquant.{source}",msg["msg"])

def critical_error_(ntype:str,source:str=""):
    """
    Specific critical errors function for this file
    """
    critical_error(ntype, f"API.market.{source}")

def error_(etype:str,source:str,msg:str):
    """
    Specific general errors function for this file
    """
    error(etype, f"API.market.{source}", msg)

def log_(ltype:str,msg:str,source:str=""):
    """
    Specific log function for this file
    """
    log(ltype,msg, f"API.market.{source}")

# ==================================================================
# Binance Single Public API Class
# ==================================================================
class SINGLE_API():
    def __init__(self,coin:str,platform_name:str='Binance'):

        # Vars ---
        self.coin = coin
        self.async_tasks = []
        self.adopted_symbols = {"TRADES":[], "OB":[]}
        self.adopted_uuids = {"TRADES":[], "OB":[]}
        self.symbole_data = {"symbols":[],"are_symboles_ready":False}
        self.platform_name = platform_name
        self.self_obj_name = "SINGLE_API"

        # REST Session ---
        self.rest_session = None
        self.trades_queue = QueueStream()
        AsyncController.window_m(self, event="add")

        # Initialyze platform
        if self.platform_name not in SYMBOLS_DATA:
            SYMBOLS_DATA[self.platform_name] = {}


    # Public functions ======================================================
    # -----------------------------------------------------------------------

    @staticmethod
    async def get_symbols():
        url = "https://api.binance.com/api/v3/exchangeInfo"
        log_("debug", "Getting symbols from Binance API...", "single_api.get_symbols")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    status = response.status

                    if status == 200:
                        data = await response.json()
                        spot_symbols = [
                            s["symbol"]
                            for s in data.get("symbols", [])
                            if s.get("isSpotTradingAllowed")
                            and str(s.get("symbol")).endswith("USDT")
                        ]
                        return spot_symbols

                    elif status == 429:
                        critical_error_("429","single_api.get_symbols")
                    elif status == 418:
                        critical_error_("418","single_api.get_symbols")
                    elif status == 403:
                        critical_error_("403","single_api.get_symbols")
                    else:
                        error_("HTTP_ERROR","single_api.get_symbols",f"Unexpected HTTP status code: {status}")

        except aiohttp.ClientError as e:
            critical_error_("0","single_api.get_symbols")
        except Exception as e:
            error_("UNKNOWN","single_api.get_symbols",f"{e}")

        return None

    # OrderBook --------------------------------------------------
    # Initialyze functions to start orderbook --------
    async def orderbook_initialyze(self,limit: int = 5000):
        log_("debug",f"Starting orderbook streams for all symbols of the coin {self.coin}...", f"{self.self_obj_name}.orderbook_initialyze")
        while True:
            if self.symbole_data["are_symboles_ready"]:
                for s in self.symbole_data["symbols"]:
                    self.async_tasks.append(asyncio.create_task(self._one_symbol_orderbook_stream(s, limit=limit)))
                break
            await asyncio.sleep(1)

    # Get the orderbook data from client ---------
    async def recv_orderbook(self,t:float=1):
        await asyncio.sleep(max(t,1.5))
        symbols_needed = self.symbole_data['symbols']
        log_("debug",f"Getting orderbook data for symbols {symbols_needed}...", f"{self.self_obj_name}.recv_orderbook")
        try:
            connections = 0
            for symbol in symbols_needed:
                if SYMBOLS_DATA[self.platform_name][symbol]["status"]["OB"] == "open":
                    connections += 1
            self.orderbook = {
                    "connections":connections,
                    "symbols":symbols_needed,
                    "asks":{}, "bids":{}
                }
            for s in symbols_needed:
                ob_data = SYMBOLS_DATA[self.platform_name][s]["orderbook"]

                for p,q in ob_data["asks"].items():
                    if p in self.orderbook["asks"].keys():
                        self.orderbook["asks"][p] = self.orderbook["asks"][p] + q
                    else:
                        self.orderbook["asks"][p] = q
                for p,q in ob_data["bids"].items():
                    if p in self.orderbook["bids"].keys():
                        self.orderbook["bids"][p] = self.orderbook["bids"][p] + q
                    else:
                        self.orderbook["bids"][p] = q
            return self.orderbook
        except Exception as e:
            error_("UNKNOWN",f"{self.self_obj_name}.recv_orderbook",f"{e}")

    # Trades ----------------------------------------------------
    # Initialyze functions to start trades --------
    async def trades_initialyze(self):
        log_("debug",f"Starting trades streams for all symbols of the coin {self.coin}...", f"{self.self_obj_name}.trades_initialyze")
        trades_sub = self.trades_queue.subscribe()
        for s in self.symbole_data["symbols"]:
            self.async_tasks.append(asyncio.create_task(self._one_symbol_trades_stream(s)))
            self.async_tasks.append(asyncio.create_task(self._one_symbol_trade_redirect(s)))
        return trades_sub

    # Get the trades from client ---------
    async def recv_trade(self,trades_sub:asyncio.Queue):
        symbols_needed = self.symbole_data['symbols']
        log_("debug",f"Getting trades data for the symbols {symbols_needed}...", f"{self.self_obj_name}.recv_trade")
        msg = await trades_sub.get()
        trades_sub.task_done()
        return msg

    # Backend functions ======================================================
    # ------------------------------------------------------------------------

    # Redirect one symbol trade's message to local trades_queue
    async def _one_symbol_trade_redirect(self,symbol:str):
        sub:asyncio.Queue = SYMBOLS_DATA[self.platform_name][symbol]["trades_stream"].subscribe()
        log_("debug",f"Starting trade redirect for symbol: {symbol}...", f"{self.self_obj_name}._one_symbol_trade_redirect")
        while True:
            msg = await sub.get()
            sub.task_done()
            await self.trades_queue.put(msg)

    # One symbol trades stream -----------------------------------------------
    async def _one_symbol_trades_stream(self, symbol: str):
        try:
            log_("debug",f"Starting trades stream for symbol: {symbol}...", f"{self.self_obj_name}._one_symbol_trades_stream")
            UUID = uuid_gen(pref="trades",sufx=self.coin,rotations=10)
            SYMBOLS_DATA[self.platform_name][symbol]["operations_queue"]["TRADES"].append(UUID)
            self.adopted_uuids["TRADES"].append(UUID)
            while True:
                if SYMBOLS_DATA[self.platform_name][symbol]["status"]["TRADES"] == "closed" and SYMBOLS_DATA[self.platform_name][symbol]["operations_queue"]["TRADES"].index(UUID) == 0:
                    try:
                        SYMBOLS_DATA[self.platform_name][symbol]["operations_queue"]["TRADES"].remove(UUID)
                        SYMBOLS_DATA[self.platform_name][symbol]["status"]["TRADES"] = "open"
                        self.adopted_symbols["TRADES"].append(symbol)
                        if UUID in self.adopted_uuids["TRADES"]:
                            self.adopted_uuids["TRADES"].remove(UUID)
                        s_obj = SYMBOLS_DATA[self.platform_name][symbol]["one_symbol_obj"]
                        await s_obj.start()
                        AsyncController.window_m(s_obj, event="add")
                        AsyncController.rest_m(s_obj.rest_session, event="add")
                        async for trade in s_obj.trades_stream():
                            await SYMBOLS_DATA[self.platform_name][symbol]["trades_stream"].put(trade)
                    except Exception as e:
                        SYMBOLS_DATA[self.platform_name][symbol]["status"]["TRADES"] = "closed"
                        SYMBOLS_DATA[self.platform_name][symbol]["operations_queue"]["TRADES"].append(UUID)
                        if symbol in self.adopted_symbols["TRADES"]:
                            self.adopted_symbols["TRADES"].remove(symbol)
                        self.adopted_uuids["TRADES"].append(UUID)
                        continue

                await asyncio.sleep(1)
        except Exception as e:
            error_("UNKNOWN",f"{self.self_obj_name}._one_symbol_trades_stream",f"{e}")

    # One symbol orderbook stream -----------------------------------------------
    async def _one_symbol_orderbook_stream(self, symbol: str, limit: int = 5000):
        try:
            log_("debug",f"Starting orderbook stream for symbol: {symbol}...", f"{self.self_obj_name}._one_symbol_orderbook_stream")
            UUID = uuid_gen(pref="orderbook",sufx=self.coin,rotations=10)
            SYMBOLS_DATA[self.platform_name][symbol]["operations_queue"]["OB"].append(UUID)
            self.adopted_uuids["OB"].append(UUID)
            while True:
                if SYMBOLS_DATA[self.platform_name][symbol]["status"]["OB"] == "closed" and SYMBOLS_DATA[self.platform_name][symbol]["operations_queue"]["OB"].index(UUID) == 0:
                    try:
                        SYMBOLS_DATA[self.platform_name][symbol]["operations_queue"]["OB"].remove(UUID)
                        SYMBOLS_DATA[self.platform_name][symbol]["status"]["OB"] = "open"
                        self.adopted_symbols["OB"].append(symbol)
                        if UUID in self.adopted_uuids["OB"]:
                            self.adopted_uuids["OB"].remove(UUID)
                        s_obj = SYMBOLS_DATA[self.platform_name][symbol]["one_symbol_obj"]
                        await s_obj.start()
                        AsyncController.window_m(s_obj, event="add")
                        AsyncController.rest_m(s_obj.rest_session, event="add")
                        async for ob in s_obj.orderbook_stream(limit=limit):
                            SYMBOLS_DATA[self.platform_name][symbol]["orderbook"]["asks"] = ob["asks"]
                            SYMBOLS_DATA[self.platform_name][symbol]["orderbook"]["bids"] = ob["bids"]
                    except Exception as e:
                        SYMBOLS_DATA[self.platform_name][symbol]["status"]["OB"] = "closed"
                        SYMBOLS_DATA[self.platform_name][symbol]["operations_queue"]["OB"].append(UUID)
                        if symbol in self.adopted_symbols["OB"]:
                            self.adopted_symbols["OB"].remove(symbol)
                        self.adopted_uuids["OB"].append(UUID)
                        continue

                await asyncio.sleep(1)
        except Exception as e:
            error_("UNKNOWN",f"{self.self_obj_name}._one_symbol_orderbook_stream",f"{e}")

    # Main Functions ========================================================

    # Initialize the API class
    async def initialize(self):
        self.coin = self.coin+"USDT"
        self.rest_session = aiohttp.ClientSession()
        log_("debug", f"Initializing {self.self_obj_name} object...", f"{self.self_obj_name}.initialize")
        AsyncController.rest_m(self.rest_session, event="add")
        # Initialyze symbole data
        symbol = self.coin
        self.symbole_data["symbols"].append(symbol)
        for i in STABLECOINS_USD:
            if i in symbol:
                asset_coin = i
                break
        SYMBOLS_DATA[self.platform_name][symbol] = {
            "base_asset": symbol,
            "quote_asset": asset_coin,
            "status": {
                "OB": "closed",
                "TRADES": "closed"
            },
            "operations_queue":{
                "OB": [],
                "TRADES": []
            },
            "one_symbol_obj": PLATFORMS_OBJS[self.platform_name]["OneSymbole"](symbol,errors_queue=Connection_errors),
            "orderbook": {"asks": {}, "bids": {}},
            "trades_stream":QueueStream()
        }
        self.symbole_data["are_symboles_ready"] = True

    # Cancel all class -------------------------------------------

    # Cancel adoption of coins
    async def _cancel_adoption(self):
        log_("debug", "Canceling adoption of coins...", f"{self.self_obj_name}._cancel_adoption")
        for s in self.adopted_symbols["TRADES"]:
            if s in SYMBOLS_DATA[self.platform_name]:
                SYMBOLS_DATA[self.platform_name][s]["status"]["TRADES"] = "closed"
                for uuid in self.adopted_uuids["TRADES"]:
                    if uuid in SYMBOLS_DATA[self.platform_name][s]["operations_queue"]["TRADES"]:
                        SYMBOLS_DATA[self.platform_name][s]["operations_queue"]["TRADES"].remove(uuid)

        for s in self.adopted_symbols["OB"]:
            if s in SYMBOLS_DATA[self.platform_name]:
                SYMBOLS_DATA[self.platform_name][s]["status"]["OB"] = "closed"
                for uuid in self.adopted_uuids["OB"]:
                    if uuid in SYMBOLS_DATA[self.platform_name][s]["operations_queue"]["OB"]:
                        SYMBOLS_DATA[self.platform_name][s]["operations_queue"]["OB"].remove(uuid)

    # Close all DEFs
    async def close(self):
        log_("debug", "Closing all connections...", f"{self.self_obj_name}.close")
        await self._cancel_adoption()
        await self.rest_session.close()
        for task in self.async_tasks:
            task.cancel()
        AsyncController.window_m(self, event="delete")