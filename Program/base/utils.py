""" 
This file contains various utility constants and configurations for the application.
"""

# ==================================================================
# Import nessary modules
# ==================================================================
import asyncio
from datetime import datetime
import random
import re
import string
import pyqtgraph as pg


# ==================================================================
# Variables
# ==================================================================

# Time frames for charting and analysis
TIME_FRAMES_INTERVALS = [
        "1m", "3m", "5m", "15m", "30m",
        "1h", "2h", "4h", "6h", "8h", "12h",
        "1d", "3d",
        "1w",
        "1M"
    ]

# List of color names supported by Qt for styling purposes
qt_color_names = [
    "aliceblue", "antiquewhite", "aqua", "aquamarine", "azure",
    "beige", "bisque", "black", "blanchedalmond", "blue",
    "blueviolet", "brown", "burlywood", "cadetblue", "chartreuse",
    "chocolate", "coral", "cornflowerblue", "cornsilk", "crimson",
    "cyan", "darkblue", "darkcyan", "darkgoldenrod", "darkgray",
    "darkgreen", "darkgrey", "darkkhaki", "darkmagenta", "darkolivegreen",
    "darkorange", "darkorchid", "darkred", "darksalmon", "darkseagreen",
    "darkslateblue", "darkslategray", "darkslategrey", "darkturquoise", "darkviolet",
    "deeppink", "deepskyblue", "dimgray", "dimgrey", "dodgerblue",
    "firebrick", "floralwhite", "forestgreen", "fuchsia", "gainsboro",
    "ghostwhite", "gold", "goldenrod", "gray", "green",
    "greenyellow", "grey", "honeydew", "hotpink", "indianred",
    "indigo", "ivory", "khaki", "lavender", "lavenderblush",
    "lawngreen", "lemonchiffon", "lightblue", "lightcoral", "lightcyan",
    "lightgoldenrodyellow", "lightgray", "lightgreen", "lightgrey", "lightpink",
    "lightsalmon", "lightseagreen", "lightskyblue", "lightslategray", "lightslategrey",
    "lightsteelblue", "lightyellow", "lime", "limegreen", "linen",
    "magenta", "maroon", "mediumaquamarine", "mediumblue", "mediumorchid",
    "mediumpurple", "mediumseagreen", "mediumslateblue", "mediumspringgreen", "mediumturquoise",
    "mediumvioletred", "midnightblue", "mintcream", "mistyrose", "moccasin",
    "navajowhite", "navy", "oldlace", "olive", "olivedrab",
    "orange", "orangered", "orchid", "palegoldenrod", "palegreen",
    "paleturquoise", "palevioletred", "papayawhip", "peachpuff", "peru",
    "pink", "plum", "powderblue", "purple", "red",
    "rosybrown", "royalblue", "saddlebrown", "salmon", "sandybrown",
    "seagreen", "seashell", "sienna", "silver", "skyblue",
    "slateblue", "slategray", "slategrey", "snow", "springgreen",
    "steelblue", "tan", "teal", "thistle", "tomato",
    "turquoise", "violet", "wheat", "white", "whitesmoke",
    "yellow", "yellowgreen"
]

# List of stablecoins pegged to the US Dollar, commonly used in cryptocurrency trading and DeFi applications
STABLECOINS_USD = [
    "USDT",   # TETHER — أَكْبَر وَأَشْهَر STABLECOIN (~1$) :CONTENTREFERENCE[OAICITE:1]{INDEX=1}
    "USDC",   # USD COIN — مُسْتَقِرَّة وَمَدْعُومَة بِأَصُول (~1$) :CONTENTREFERENCE[OAICITE:2]{INDEX=2}
    "BUSD",   # BINANCE USD — مُسْتَقِرَّة (~1$) :CONTENTREFERENCE[OAICITE:3]{INDEX=3}
    "DAI",    # DAI — مُسْتَقِرَّة لامَرْكَزِيَّة (~1$) :CONTENTREFERENCE[OAICITE:4]{INDEX=4}
    "TUSD",   # TRUEUSD — مُسْتَقِرَّة (~1$) :CONTENTREFERENCE[OAICITE:5]{INDEX=5}
    "USDP",   # PAX DOLLAR — مُسْتَقِرَّة (~1$) :CONTENTREFERENCE[OAICITE:6]{INDEX=6}
    "PYUSD",  # PAYPAL USD — مُسْتَقِرَّة (~1$) :CONTENTREFERENCE[OAICITE:7]{INDEX=7}
    "USDE",   # ETHENA USDE — مُسْتَقِرَّة (~1$) حَسْب القِيمَة السُّوقِيَّة :CONTENTREFERENCE[OAICITE:8]{INDEX=8}
    "USD1",   # WORLD LIBERTY USD — مُسْتَقِرَّة (~1$) :CONTENTREFERENCE[OAICITE:9]{INDEX=9}
    "FDUSD",  # FIRST DIGITAL USD — مُسْتَقِرَّة (~1$) :CONTENTREFERENCE[OAICITE:10]{INDEX=10}
    "RLUSD",  # RIPPLE USD — مُسْتَقِرَّة مَدْعُومَة (~1$) :CONTENTREFERENCE[OAICITE:11]{INDEX=11}
    "USDD",   # TRON DAO STABLECOIN (~1$, قَد يَكُون ALGORITHMIC) :CONTENTREFERENCE[OAICITE:12]{INDEX=12}
    "OUSD",   # ORIGIN DOLLAR (~1$, DEFI STABLE) :CONTENTREFERENCE[OAICITE:13]{INDEX=13}
    "USDX",   # USDX — STABLECOIN خَاص مِن بَعْض الشَبَكَات (~1$) :CONTENTREFERENCE[OAICITE:14]{INDEX=14}
    "MUSD",   # MSTALE USD (~1$, DEFI) :CONTENTREFERENCE[OAICITE:15]{INDEX=15}
    "VAI",    # VAI — STABLECOIN (~1$) مِن بَعْض الشَبَكَات :CONTENTREFERENCE[OAICITE:16]{INDEX=16}
    "CUSDC",  # CELO USD COIN (~1$) — نُسْخَة USDC عَلَى CELO BLOCKCHAIN :CONTENTREFERENCE[OAICITE:17]{INDEX=17}
    "SEP20_USDX", # نُسْخَة USDX عَلَى بَعْض الشَبَكَات :CONTENTREFERENCE[OAICITE:18]{INDEX=18}
    # إِضَافَات قَد لا تَكُون كَبِيرَة فِي السَّيُولَة لَكِنَّهَا تُعَدُّ مُسْتَقِرَّة بِمُحَاوَلَة الحِفَاظ عَلَى ~1$
    "RSV",    # RESERVE (قَد يَكُون جُزْءًا مِن بِنْيَة STABLECOLLATERAL) :CONTENTREFERENCE[OAICITE:19]{INDEX=19}
    "SUSD",   # SYNTH SUSD — مُسْتَقِرَّة (~1$) فِي نُظُم السِّينثِتِيكْس :CONTENTREFERENCE[OAICITE:20]{INDEX=20}
    "CUSD",   # CELO DOLLAR (~1$, تِقْنِيَّة DEFI) :CONTENTREFERENCE[OAICITE:21]{INDEX=21}
    "USNFT",  # بَعْض مَشَارِيع NFT تَرْبِط قِيمَة رُمُوزَهَا بِ 1$ — ضَعِيف السَّيُولَة :CONTENTREFERENCE[OAICITE:22]{INDEX=22}
    "BIF",    # بَعْض نُسَخ مُسْتَقِرَّة مَحَلِّيَّة فِي سَلاَسِل بَعِيدَة (~1$) :CONTENTREFERENCE[OAICITE:23]{INDEX=23}
    # بَقِيَّة الرُّمُوز ذُكِرَت فِي المُجْتَمَعَات كَـ “STABLECOINS” لَكِنَّ كَثِيرًا مِنْهَا لَيْسَ مَدْعُومًا بِنَفْس الثَّبَات
    "MUSD",   # MSTALE USD — STABLECOIN DEFI (~1$) :CONTENTREFERENCE[OAICITE:24]{INDEX=24}
    "USN",    # USN — STABLECOIN مُرْتَبِط بِ NEAR ECOSYSTEM (~1$) :CONTENTREFERENCE[OAICITE:25]{INDEX=25}
    "USBZ",   # STABLECOIN تَجْرِيبِي فِي بَعْض السَّلاَسِل (~1$) :CONTENTREFERENCE[OAICITE:26]{INDEX=26}
    "NUSD",   # STABLECOIN عَلَى بَعْض الشَبَكَات (~1$) :CONTENTREFERENCE[OAICITE:27]{INDEX=27}
    "USDQ",   # STABLECOIN فِي بَعْض الْمَنَصَّات (~1$) :CONTENTREFERENCE[OAICITE:28]{INDEX=28}
    "USDH",   # USDH — STABLECOIN عَلَى بَعْض الشَبَكَات (~1$) :CONTENTREFERENCE[OAICITE:29]{INDEX=29}
    "SEURO",  # عَادَةً مُسْتَقِرَّة مُقَابِل اليُورُو لَكِنَّهَا قَد تُبْنَى لِلقِيمَة (~1$) :CONTENTREFERENCE[OAICITE:30]{INDEX=30}
    "FRAX",   # FRAX — HYBRID STABLE (~≈1$) :CONTENTREFERENCE[OAICITE:31]{INDEX=31}
    "FEI",    # FEI USD — STABLECOIN لَكِنَّهُ قَد يَخْرُج عَنِ الـ PEG أَحْيَانًا :CONTENTREFERENCE[OAICITE:32]{INDEX=32}
    "HUSD",   # HUSD — STABLECOIN مَدْعُوم فِي بَعْض الْمَنَصَّات (~1$) :CONTENTREFERENCE[OAICITE:33]{INDEX=33}
    "USK",    # USK — STABLECOIN فِي بَعْض الْبَرُوتُوكُولَات (~1$) :CONTENTREFERENCE[OAICITE:34]{INDEX=34}
    "RISD",   # مَشْرُوع STABLECOIN أَقَل شُعْبِيَّة (~1$) :CONTENTREFERENCE[OAICITE:35]{INDEX=35}
    "USX",    # STABLECOIN مُرَكَّب (~1$) :CONTENTREFERENCE[OAICITE:36]{INDEX=36}
    "SEURO",  # STABLECOIN مُقَابِل اليُورُو لَكِنْ يَظْهَر فِي قَوَائِم STABLE (~1$) :CONTENTREFERENCE[OAICITE:37]{INDEX=37}
    "XUSD",   # XUSD — STABLECROSS (~1$) :CONTENTREFERENCE[OAICITE:38]{INDEX=38}
    "LUSD",   # LIQUITY USD — STABLE (~1$) :CONTENTREFERENCE[OAICITE:39]{INDEX=39}
    "HUSD",   # HUOBI USD — STABLE عَبْر بَعْض الْمَنَصَّات (~1$) :CONTENTREFERENCE[OAICITE:40]{INDEX=40}
    "PYRUSD", # رَمْز STABLE مُسْتَخْرَج فِي بَعْض السَّلاَسِل (~1$) :CONTENTREFERENCE[OAICITE:41]{INDEX=41}
]


NO_INTERNET_EXEPTIONS = [
    "aiohttp.client_exceptions.ClientConnectorError",
    "aiohttp.client_exceptions.ClientOSError",
    "websockets.exceptions.ConnectionClosed",
    "websockets.exceptions.InvalidHandshake",
    "builtins.OSError",
    'aiohttp.client_exceptions.ClientConnectorDNSError',
    "websockets.exceptions.ConnectionClosedError",
    'gaierror',
    
]

# ==================================================================
# Functions
# ==================================================================

# Gen UUid for any def -------
def uuid_gen(pref:str=None,sufx:str=None,rotations:int=4):
    strings = string.ascii_letters + string.digits
    d1 = lambda: ''.join([random.choice(strings) for _ in range(5)])
    gg = '-'.join([d1() for _ in range(rotations)])
    if pref: gg = pref+'--'+gg
    if sufx: gg = gg+'--'+sufx
    return gg

# Convert timestamp (milliseconds) to human-readable date string
DATE = lambda v: datetime.fromtimestamp(v / 1000).strftime("%Y-%m-%d %H:%M:%S")

# Function to convert time frame strings to milliseconds
def to_milliseconds(frame: str):
    """
    Convert a time frame string (e.g., '5min', '1h') into milliseconds.
    :param frame: String containing number and unit (ms, s, min, h, d, w, M)
    :return: Tuple (milliseconds, unit_string)
    """
    # Mapping of units to (milliseconds, short label)
    units = {
        "ms": [1, "ms"],              # milliseconds
        "s": [1000, "s"],             # seconds
        "min": [60000, "m"],          # minutes
        "m": [60000, "m"],          # minutes
        "h": [3600000, "h"],          # hours
        "d": [86400000, "d"],         # days
        "w": [604800000, "w"],        # weeks
        "M": [2592000000, "M"],       # months (approximate)
    }

    # Match pattern like "15min", "1h", "500ms"
    match = re.match(r"(\d+)(ms|s|min|m|h|d|w|M)", frame)
    if not match:
        raise ValueError("The time frame is not correct")

    # Extract numeric value and unit
    value, unit = match.groups()

    # Convert value to milliseconds and return with unit label
    return int(value) * units[unit][0], str(value) + str(units[unit][1])




# ==================================================================
# Classes
# ==================================================================

# Custom time axis for pyqtgraph plots
class TimeAxis(pg.AxisItem):
    """Custom time axis for pyqtgraph plots"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Initialize base AxisItem

    def tickStrings(self, values, scale, spacing):
        """
        Override default tick labels to display time format.
        :param values: List of tick positions (in ms)
        :param scale: Scale factor for the axis
        :param spacing: Tick spacing
        :return: List of formatted date strings
        """
        out = []
        for v in values:
            try:
                out.append(DATE(v))  # Convert timestamp to date string
            except Exception:
                out.append("")  # Fallback for invalid values
        return out
    
# A simple implementation of a pub-sub queue using janus for asynchronous communication
class QueueStream:
    def __init__(self):
        self.subscribes: list = []

    def subscribe(self) : 
        q = asyncio.Queue()
        self.subscribes.append(q)
        return q

    def unsuscribe(self,sub) -> bool :
        if sub in self.subscribes:
            self.subscribes.remove(sub)
            return True
        else:
            return False
        
    async def put(self,msg:...):
        await asyncio.gather(*(sub.put(msg) for sub in self.subscribes))

    def send(self, msg: dict):
        asyncio.create_task(self.put(msg))

# A more advanced implementation of a pub-sub queue that allows for multiple channels and categorization of messages
class QueueStreamChannel():
    def __init__(self):
        self.subscribes: dict = {'all':[]}

    # Subscribe to a channel and receive an async queue for that channel. Multiple subscribers can subscribe to the same channel.
    def subscribe(self,channel:str):
        q = asyncio.Queue(maxsize=100)
        if channel not in self.subscribes:
            self.subscribes[channel] = []
        self.subscribes[channel].append(q)
        return q
    

    # Unsuscribe from a channel. If the subscriber is the last one for that channel, the channel is removed from the subscribes dictionary.
    def unsuscribe(self,sub,channel:str) -> bool :
        if channel in self.subscribes:
            if sub in self.subscribes[channel]:
                self.subscribes[channel].remove(sub)
            else:
                return False
            if len(self.subscribes[channel]) == 0:
                del self.subscribes[channel]
            return True
        else:
            return False
        
    # Put a message in the channel's queue for all subscribers of that channel. If the channel does not exist, the message is not sent.
    async def put(self,msg:dict):
        channel = msg.get("event","")
        if channel in self.subscribes:
            await asyncio.gather(*(sub.put(msg) for sub in self.subscribes[channel]))
        await asyncio.gather(*(sub.put(msg) for sub in self.subscribes['all']))

    # Send a message to the channel's queue for all subscribers of that channel. This is a non-blocking call that creates an asyncio task to put the message in the queue.
    def send(self, msg: dict):
        asyncio.create_task(self.put(msg))