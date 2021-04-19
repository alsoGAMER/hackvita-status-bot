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

import logging

from pyrogram.session import Session

from BotBase.config import bot, LOGGING_LEVEL, LOGGING_FORMAT, DATE_FORMAT
from BotBase.database.raw_queries import CREATE_USERS_TABLE
from BotBase.database.query import create_table

if __name__ == "__main__":
    logging.basicConfig(format=LOGGING_FORMAT, datefmt=DATE_FORMAT, level=LOGGING_LEVEL)
    Session.notice_displayed = True
    try:
        logging.warning("Running create_table()")
        create_table(CREATE_USERS_TABLE)
        logging.warning("Database interaction complete")
        logging.warning("Starting bot")
        bot.run()
    except Exception as e:
        logging.warning(f"Stopping bot due to a {type(e).__name__}: {e}")
        bot.stop()
