# ==================================================================
# Import nessary modules
# ==================================================================

# == Libs ==
import sys
import os

# == Program Modules ==
from base.files_folders import *


# ==================================================================
# Create folders if they don't exist
# ==================================================================
os.makedirs(APP_DATA,exist_ok=True)
os.makedirs(os.path.join(APP_DATA,'data',"users"),exist_ok=True)
os.makedirs(PLUGINS_DIR,exist_ok=True)
os.makedirs(MORE_PACKAGES,exist_ok=True)

os.makedirs(ASSETS,exist_ok=True)
os.makedirs(ASSETS_HTML,exist_ok=True)
os.makedirs(ASSETS_CSS,exist_ok=True)
os.makedirs(ASSETS_QSS,exist_ok=True)
os.makedirs(ASSETS_ICONS,exist_ok=True)
os.makedirs(ASSETS_ICONS_SVG,exist_ok=True)
os.makedirs(ASSETS_ICONS_ICO,exist_ok=True)

sys.path.append(MORE_PACKAGES)