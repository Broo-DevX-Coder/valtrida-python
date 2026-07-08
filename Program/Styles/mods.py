# ==================================================================
# Import nessary modules
# ==================================================================

# == local ==
from config import COLOR_MODE
from . import DARK_TO_LIGHT_COLORS
from . import plot_styles


# ==================================================================
# Helper functions
# ==================================================================
def change_to_light_mode(content:str):
    for dark,light in DARK_TO_LIGHT_COLORS.items():
        if dark in content:
            content = content.replace(dark, light)
    
    return content


# ==================================================================
# Exection
# ==================================================================
if COLOR_MODE == "light":
    from .qss import QSS
    from .css import CSS

    QSS["BINANCE"] = change_to_light_mode(QSS["BINANCE"])
    QSS["MAIN_W_TOOL_BAR"] = change_to_light_mode(QSS["MAIN_W_TOOL_BAR"])
    QSS["POPUP_W"] = change_to_light_mode(QSS["POPUP_W"])
    QSS["AUTH_TOOL_BAR"] = change_to_light_mode(QSS["AUTH_TOOL_BAR"])
    CSS["MAIN"] = change_to_light_mode(CSS["MAIN"])