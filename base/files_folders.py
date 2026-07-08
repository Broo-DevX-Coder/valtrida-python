# ==================================================================
# Import nessary modules
# ==================================================================

# == Libs ==
from pathlib import Path
import os
import tempfile

# == Local ==
from config import *

# ==================================================================
# Set files and folders paths
# ==================================================================
APP_DATA = os.path.join(Path.home(),f".{APP_NAME}")
USERS_FILE = os.path.join(APP_DATA,'data',"users")
PLUGINS_DIR = os.path.join(APP_DATA,"Plugins")
TEMP_FILE = tempfile.mkdtemp()
MORE_PACKAGES = os.path.join(APP_DATA,"Packages")

ASSETS = os.path.join(APP_DATA,"ASSETS")
ASSETS_HTML = os.path.join(APP_DATA,"ASSETS","html")
ASSETS_CSS = os.path.join(APP_DATA,"ASSETS","css")
ASSETS_QSS = os.path.join(APP_DATA,"ASSETS","qss")
ASSETS_ICONS = os.path.join(APP_DATA,"ASSETS","icons")
ASSETS_ICONS_SVG = os.path.join(APP_DATA,"ASSETS","icons","svg")
ASSETS_ICONS_ICO = os.path.join(APP_DATA,"ASSETS","icons","ico")