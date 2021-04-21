"""
    HackVita Status Bot: Monitor HackVita.eu status with ease
    Copyright (C) 2021  alsoGAMER

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import platform
from collections import defaultdict

import MySQLdb
from plate import Plate
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# region Antiflood module configuration
# The antiflood works by accumulating up to MAX_UPDATE_THRESHOLD updates (user-wise) and
# when that limit is reached, perform some checks to tell if the user is actually flooding

BAN_TIME = 300
# The amount of seconds the user will be banned
MAX_UPDATE_THRESHOLD = 7
# How many updates to accumulate before starting to count
PRIVATE_ONLY = True
# If True, the antiflood will only work in private chats
FLOOD_PERCENTAGE = 75
# The percentage (from 0 to 100) of updates that when below ANTIFLOOD_SENSIBILITY will trigger the anti flood
# Example, if FLOOD_PERCENTAGE == 75, if at least 75% of the messages from a user are marked as flood it will be blocked
ANTIFLOOD_SENSIBILITY = 1
# The minimum amount of seconds between updates. Updates that are sent faster than this limit will trigger the antiflood
# This should not be below 1, but you can experiment if you feel bold enough
DELETE_MESSAGES = True
# Set this to false if you do not want the messages to be deleted after flood is detected
FLOOD_NOTICE = True
# Set this to false if you do not want to notify the user that has been flood-banned
BYPASS_FLOOD = True
# If False, admins can be flood-blocked too, otherwise the antiflood will ignore them
# endregion

# region Various options and global variables

CACHE = defaultdict(lambda: ["none", 0])
# Global cache. DO NOT TOUCH IT, really just don't
NAME = "tg://user?id={}"

PY_VERSION = platform.python_version()
BOT_VERSION = "1.1a"
BOTBASE_VERSION = "2.1.1"
# endregion

# region Telegram client configuration

WORKERS_NUM = 15
# The number of worker threads that pyrogram will spawn at the startup.
# 15 workers means that the bot will process up to 15 users at the same time and then block until one worker has done

BOT_TOKEN = ""
# Get it with t.me/BotFather
SESSION_NAME = "hackvita-status-bot"
# The name of the Telegram Session that the bot will have, will be visible from Telegram
PLUGINS_ROOT = {"root": f"BotBase/modules"}
# Do not change this unless you know what you're doing
API_ID = 000000
# Get it at https://my.telegram.org/apps
API_HASH = ""
# Same as above
DEVICE_MODEL = "hackvita-status-bot"
# Name of the device shown in the sessions list - useless for a Bot
SYSTEM_VERSION = "1.1a"
# Host OS version, can be the same as VERSION - also useless for a Bot
LANG_CODE = "en_US"
# Session lang_code
bot = Client(
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=PLUGINS_ROOT,
    session_name=SESSION_NAME,
    workers=WORKERS_NUM,
    device_model=DEVICE_MODEL,
    system_version=SYSTEM_VERSION,
    lang_code=LANG_CODE,
)
plate = Plate(root="BotBase/locales")
# endregion

# region Logging configuration
# To know more about what these options mean, check https://docs.python.org/3/library/logging.html

LOGGING_FORMAT = (
    "[%(levelname)s %(asctime)s] In thread '%(threadName)s', "
    f"module %(module)s, function %(funcName)s at line %(lineno)d -> [{SESSION_NAME}] %(message)s"
)
DATE_FORMAT = "%d/%m/%Y %H:%M:%S %p"
LOGGING_LEVEL = 30
# endregion

# region Start module
# P.S.: {mention} in the GREET message will be replaced with a mention to the user, same applies for {id} and {username}

GREET = True
# Set this to False if you don't want the Bot to reply to /start.
# endregion

# region Database configuration
# The only natively supported database is MariaDB, but you can easily tweak
# this section and the BotBase/database/query.py file to work with any DBMS
# If you do so and want to share your code feel free to open a PR on the repo!

DB_URL = MySQLdb.connect(
    host="127.0.0.1",
    user="",
    passwd="",
    db="",
)
# endregion

# region Greet Keyboard
BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                plate("services_status_history_button"), "services_status_history"
            ),
        ],
        [
            InlineKeyboardButton(plate("bot_disclaimer_button"), "bot_disclaimer"),
            InlineKeyboardButton(plate("about_button"), "bot_about"),
        ],
    ]
)
# This keyboard will be sent along with GREET, feel free to add or remove buttons
# endregion

# region Admin module configuration

ADMINS = {0000000: ""}
# Edit this dict adding the ID:NAME pair of the admin that you want to add. You can add as many admins as you want.
# endregion
