"""
This module holds all the constants used inside the project
"""

import pathlib

ROOT = pathlib.Path(__file__).parent

# ================================
#   Database Variables
# ================================

DATABASE_NAME = "DataBase.db"
DATABASE_FOLDER = ROOT / "database"
DATABASE_PATH = DATABASE_FOLDER / DATABASE_NAME

# ================================
#   Logging Variables
# ================================
LOGGING_PATH = ROOT / "logs" / "log.log"

# ================================
#   Window Settings
# ================================

INTERFACE_SCHEME = "system"
THEME = "dark-blue"
APP_NAME = "Password Manager"
RESIZABLE_VALUE = (False, False)

# ================================
#   Color Settings
# ================================

GREY = "1a1a1a"
SIDEBAR_TEXT_COLOR = "#d6d6d6"

# ================================
#   Credentials Settings
# ================================
CREDENTIALS_NAME = "credentials.json"
CREDENTIALS_FOLDER = ROOT / "credentials"
CREDENTIALS_PATH = CREDENTIALS_FOLDER / CREDENTIALS_NAME