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
import time
from collections import defaultdict

from pyrogram import Client, filters

from BotBase.config import (
    ADMINS,
    ANTIFLOOD_SENSIBILITY,
    BAN_TIME,
    BYPASS_FLOOD,
    FLOOD_NOTICE,
    CACHE,
    DELETE_MESSAGES,
    FLOOD_PERCENTAGE,
    MAX_UPDATE_THRESHOLD,
    PRIVATE_ONLY,
    bot,
    plate,
)
from BotBase.methods import MethodWrapper
from BotBase.methods.custom_filters import user_banned

# Some variables for runtime configuration

MESSAGES = defaultdict(list)  # Internal variable for the antiflood module
BANNED_USERS = filters.user()  # Filters where the antiflood will put banned users
BYPASS_USERS = filters.user(list(ADMINS.keys())) if BYPASS_FLOOD else filters.user()
ADMINS = filters.user(list(ADMINS.keys()))
FILTER = filters.private if PRIVATE_ONLY else ~filters.user()
wrapper = MethodWrapper(bot)


def is_flood(updates: list):
    """
    Calculates if a sequence of
    updates corresponds to a flood
    """

    genexpr = [
        i <= ANTIFLOOD_SENSIBILITY
        for i in (
            (updates[i + 1] - timestamp)
            if i < (MAX_UPDATE_THRESHOLD - 1)
            else (timestamp - updates[i - 1])
            for i, timestamp in enumerate(updates)
        )
    ]
    return sum(genexpr) >= int((len(genexpr) / 100) * FLOOD_PERCENTAGE)


@Client.on_message(FILTER & ~BYPASS_USERS & ~user_banned(), group=-1)
async def anti_flood(_, update):
    """Anti flood module"""

    user_id = update.from_user.id
    chat = update.chat.id
    date = update.date
    message_id = update.message_id
    if isinstance(MESSAGES[user_id], tuple):
        chat, date = MESSAGES[user_id]
        if time.time() - date >= BAN_TIME:
            logging.warning(
                f"{user_id} has waited at least {BAN_TIME} seconds in {chat} and can now text again"
            )
            BANNED_USERS.remove(user_id)
            del MESSAGES[user_id]
    elif (
        len(MESSAGES[user_id]) >= MAX_UPDATE_THRESHOLD - 1
    ):  # -1 to avoid acting on the next update
        MESSAGES[user_id].append({chat: (date, message_id)})
        logging.info(
            f"MAX_UPDATE_THRESHOLD ({MAX_UPDATE_THRESHOLD}) Reached for {user_id}"
        )
        user_data = MESSAGES.pop(user_id)
        timestamps = [list(*d.values())[0] for d in user_data]
        updates = [list(*d.values())[1] for d in user_data]
        if is_flood(timestamps):
            logging.warning(f"Flood detected from {user_id} in chat {chat}")
            if user_id in CACHE:
                del CACHE[user_id]
            BANNED_USERS.add(user_id)
            # noinspection PyTypeChecker
            MESSAGES[user_id] = chat, time.time()
            if FLOOD_NOTICE:
                await wrapper.send_message(
                    user_id, plate("flood_notice", time=f"{BAN_TIME / 60:.1f}")
                )
            if DELETE_MESSAGES:
                await wrapper.delete_messages(chat, updates)
        else:
            if user_id in MESSAGES:
                del MESSAGES[user_id]
    else:
        MESSAGES[user_id].append({chat: (date, message_id)})


@Client.on_message(FILTER & ADMINS & ~filters.edited & filters.command("clearflood"))
async def clear_flood(_, message):
    if len(message.command) == 1:
        global MESSAGES  # Ew...
        MESSAGES = defaultdict(list)
        for user in BANNED_USERS.copy():
            BANNED_USERS.remove(user)
        await wrapper.send_message(message.chat.id, plate("flood_cleared"))
    else:
        for user in message.command[1:]:
            if not user.isdigit():
                return await wrapper.send_message(
                    message.chat.id, plate("error") + ":" + plate("non_numeric_id")
                )
            BANNED_USERS.discard(int(user))
            # noinspection PyUnboundLocalVariable
            MESSAGES.pop(int(user), None)
        await wrapper.send_message(
            message.chat.id,
            plate(
                "flood_user_cleared",
                user=", ".join((f"{usr}" for usr in message.command[1:])),
            ),
        )
