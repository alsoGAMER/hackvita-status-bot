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

import re

from pyrogram import filters

from BotBase.database.query import check_banned


def check_user_banned(tg_id: int):
    res = check_banned(tg_id)
    if isinstance(res, Exception):
        return False
    else:
        if not res:
            return False
        return bool(res[0])


def callback_regex(pattern: str):
    return filters.create(lambda flt, client, update: re.match(pattern, update.data))


def user_banned():
    return filters.create(
        lambda flt, client, update: check_user_banned(update.from_user.id)
    )


def is_command():
    return filters.create(
        lambda flt, client, message: all(
            (
                message.text,
                [
                    message.text[entity.offset : entity.offset + entity.length]
                    for entity in message.entities or []
                    if entity.type == "bot_command"
                ],
            )
        )
    )
