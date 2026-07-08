import pyqtgraph as pg
from PySide2.QtGui import *
from config import COLOR_MODE
from . import DARK_TO_LIGHT_COLORS

COL = lambda x: DARK_TO_LIGHT_COLORS[x] if x in DARK_TO_LIGHT_COLORS.keys() and COLOR_MODE == "light" else x

def binance_charts_theme():
    # Background
    pg.setConfigOption("background", COL("#0d0f1a"))
    
    # النصوص والمحاور (رمادي مزرق فاتح)
    pg.setConfigOption("foreground", COL("#AAB0C6"))
    
    # لون الشبكة (كحلي أفتح شوي من الخلفية)
    pg.setConfigOption("antialias", True) 

binance_charts_theme()

class GlobalCursor():
    LABELS_BG = "#1f2640"
    def set_label_pos2(widget, value_v, value_diciamles=2):
        widget.setHtml(
            f"<div style='color:#EAECEF;padding:2px 6px;"
            f"border-radius:3px;font-size:12px;'>"
            f"{value_v:.{value_diciamles}f}</div>"
        )
        widget.fill = QBrush(QColor(COL("#1f2640")))
        widget.update()

    def set_label_pos(widget, date_str, value_n, value_v, value_diciamles=2, auther=None):
        widget.setHtml(
            "<div style='background-color:#1f2640;"
            "color:#EAECEF;border-radius:6px;"
            "padding:4px 8px;font-size:12px;'><br>"
            f"&nbsp;&nbsp;&nbsp;Date: <span style='color:#6c63ff'>{date_str}</span>&nbsp;&nbsp;&nbsp;<br>"
            f"&nbsp;&nbsp;&nbsp;{value_n}: {value_v:.{value_diciamles}f}&nbsp;&nbsp;&nbsp;"
            f"{auther if auther != None else '' }"
            "<br></div>"
        )
        widget.update()


class CandalsChart():
    def set_candals_color():
        # Candles Colors (متوافقة مع الأيقونة)
        candle_up = QColor("#0ECB81")   # أزرق صاعد
        candle_down = QColor("#F6465D") # بنفسجي هابط
        return {"candle_up": candle_up, "candle_down": candle_down}
    
    def set_price_label(widget, price, up=True, price_diciamles=2):
        color = "#0ECB81" if up else "#F6465D"   # أزرق/بنفسجي بدال الأخضر/أحمر
        widget.fill = QBrush(QColor(color))
        widget.setHtml(
            f"<div style='color:#fff;padding:2px 6px;border-radius:3px;'>"
            f"{price:.{price_diciamles}f}</div>"
        )
        widget.update()
