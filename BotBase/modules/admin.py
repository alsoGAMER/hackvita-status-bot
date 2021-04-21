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

import itertools
import logging
import random
import re

from pyrogram import Client, filters

from BotBase.config import (
    ADMINS,
    CACHE,
    NAME,
    bot,
    plate,
)
from BotBase.database.query import (
    ban_user,
    get_user,
    get_user_by_name,
    get_users,
    unban_user,
    update_name,
)
from BotBase.methods import MethodWrapper
from BotBase.modules.antiflood import BANNED_USERS

ADMINS_FILTER = filters.user(list(ADMINS.keys()))
wrapper = MethodWrapper(bot)


def format_user(user):
    (tg_id, tg_uname, date, banned) = user
    return plate(
        "user_info",
        tg_id=tg_id,
        tg_uname="@" + tg_uname if tg_uname else "N/A",
        date=date,
        status=plate("yes") if banned else plate("no"),
        admin=plate("yes") if tg_id in ADMINS else plate("no"),
    )


@Client.on_message(
    filters.command("getranduser") & ADMINS_FILTER & ~BANNED_USERS & ~filters.edited
)
async def get_random_user(_, message):
    logging.warning(
        f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /getranduser"
    )
    if len(message.command) > 1:
        await wrapper.send_message(
            message.chat.id, plate("no_parameters", command="/getranduser")
        )
    else:
        user = random.choice(get_users())
        result = get_user(*user)
        text = format_user(result)
        await wrapper.send_message(message.chat.id, text)


@Client.on_message(
    filters.command("getuser")
    & ADMINS_FILTER
    & filters.private
    & ~BANNED_USERS
    & ~filters.edited
)
async def get_user_info(_, message):
    if len(message.command) != 2:
        return await wrapper.send_message(
            message.chat.id, plate("invalid_syntax", correct="/getuser id/[@]username")
        )

    if message.command[1].isdigit():
        name = None
        user = get_user(message.command[1])
    else:
        name = message.command[1].lstrip("@").lower()
        user = get_user_by_name(name)

    if user:
        logging.warning(
            f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /getuser {message.command[1]}"
        )
        result = user
        text = format_user(result)
        await wrapper.send_message(message.chat.id, text)
    else:
        if name:
            await wrapper.send_message(
                message.chat.id,
                plate("error")
                + ":"
                + plate("name_missing", tg_uname=message.command[1]),
            )
        else:
            await wrapper.send_message(
                message.chat.id,
                plate("error") + ":" + plate("id_missing", tg_id=message.command[1]),
            )


@Client.on_message(
    filters.command("count")
    & ADMINS_FILTER
    & filters.private
    & ~BANNED_USERS
    & ~filters.edited
)
async def count_users(_, message):
    if len(message.command) > 1:
        await wrapper.send_message(
            message.chat.id, plate("no_parameters", command="/count")
        )
    else:
        logging.warning(
            f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /count"
        )
        users_count = len(get_users())
        await wrapper.send_message(message.chat.id, plate("users_count", users_count=users_count))


@Client.on_message(
    filters.command("global")
    & ADMINS_FILTER
    & filters.private
    & ~BANNED_USERS
    & ~filters.edited
)
async def global_message(_, message):
    if len(message.command) > 1:
        msg = message.text.html[7:]
        logging.warning(
            f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent the following global message: {msg}"
        )

        missed = 0
        attempts = 0

        for tg_id in itertools.chain(*get_users()):
            attempts += 1
            result = await wrapper.send_message(tg_id, msg)

            if isinstance(result, Exception):
                logging.error(
                    f"Could not deliver the global message to {tg_id} because of {type(result).__name__}: {result}"
                )
                missed += 1

        logging.warning(
            f"{attempts - missed}/{attempts} global messages were successfully delivered"
        )
        await wrapper.send_message(
            message.chat.id,
            plate(
                "global_message_stats", attempts=attempts, success=(attempts - missed), msg=msg
            ),
        )
    else:
        await wrapper.send_message(
            message.chat.id,
            plate("invalid_syntax", correct="/global message")
            + "\n<b>HTML and Markdown styling supported</b>",
        )


@Client.on_message(
    filters.command("whisper")
    & ADMINS_FILTER
    & filters.private
    & ~BANNED_USERS
    & ~filters.edited
)
async def whisper(_, message):
    if len(message.command) < 2:
        return await wrapper.send_message(
            message.chat.id,
            plate("invalid_syntax", correct="/whisper ID")
            + "\n<b>HTML and Markdown styling supported</b>",
        )

    if not message.command[1].isdigit():
        return await wrapper.send_message(
            message.chat.id, plate("error") + ":" + plate("non_numeric_id")
        )

    logging.warning(
        f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent {message.text.html}"
    )

    tg_id = int(message.command[1])
    msg = message.text.html[9:]
    msg = msg[re.search(message.command[1], msg).end() :]

    if tg_id not in itertools.chain(*get_users()):
        return await wrapper.send_message(
            message.chat.id, plate("error") + ":" + plate("id_missing", tg_id=tg_id)
        )

    result = await wrapper.send_message(
        tg_id,
        plate(
            "whisper_from",
            admin=f"[{ADMINS[message.from_user.id]}]({NAME.format(message.from_user.id)})",
            msg=msg,
        ),
    )

    if isinstance(result, Exception):
        logging.error(
            f"Could not whisper to {tg_id} because of {type(result).__name__}: {result}"
        )
        await wrapper.send_message(
            message.chat.id, plate("error") + f": {type(result).__name__} -> {result}"
        )
    else:
        await wrapper.send_message(message.chat.id, plate("whisper_successful"))


@Client.on_message(
    filters.command("update")
    & ADMINS_FILTER
    & filters.private
    & ~BANNED_USERS
    & ~filters.edited
)
async def update(_, message):
    if len(message.command) != 2:
        return await wrapper.send_message(
            message.chat.id, plate("invalid_syntax", correct="/update ID")
        )

    if not message.command[1].isdigit():
        return await wrapper.send_message(
            message.chat.id, plate("error") + ":" + plate("non_numeric_id")
        )

    user = get_user(message.command[1])
    if user:
        logging.warning(
            f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /update {message.command[1]}"
        )

        tg_id, tg_uname = user[:2]
        new = await wrapper.get_users(tg_id)

        if isinstance(new, Exception):
            logging.error(
                f"An error has occurred when calling get_users({tg_id}), {type(new).__name__}: {new}"
            )
            await wrapper.send_message(
                message.chat.id, plate("error") + f": {type(new).__name__} -> {new}"
            )
        else:
            if new.username is None:
                new.username = "null"
            if new.username != tg_uname:
                update_name(tg_id, new.username)
                await wrapper.send_message(message.chat.id, plate("user_info_updated"))
            else:
                await wrapper.send_message(
                    message.chat.id, plate("user_info_unchanged")
                )
    else:
        await wrapper.send_message(
            message.chat.id,
            plate("error") + ":" + plate("id_missing", tg_id=message.command[1]),
        )


@Client.on_message(
    filters.command(["ban", "unban"])
    & ADMINS_FILTER
    & filters.private
    & ~BANNED_USERS
    & ~filters.edited
)
async def ban(_, message):
    cmd = message.command[0]
    condition = {"ban": False, "unban": True}.get(cmd)

    if len(message.command) != 2:
        return await wrapper.send_message(
            message.chat.id, plate("invalid_syntax", correct=f"/{cmd} ID")
        )

    if not message.command[1].isdigit():
        return await wrapper.send_message(
            message.chat.id, plate("error") + ":" + plate("non_numeric_id")
        )

    if int(message.command[1]) in ADMINS:
        return await wrapper.send_message(message.chat.id, plate("cannot_ban_admin"))

    user = get_user(message.command[1])
    if user:
        if bool(user[3]) is condition:
            logging.warning(
                f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /{cmd} {message.command[1]}"
            )

            tg_id = user[0]
            if condition:
                res = unban_user(tg_id)
            else:
                res = ban_user(tg_id)

            if isinstance(res, Exception):
                logging.error(
                    f"An error has occurred when calling {cmd}_user({tg_id}), {type(res).__name__}: {res}"
                )
                await wrapper.send_message(
                    message.chat.id, plate("error") + f": {type(res).__name__} -> {res}"
                )
            else:
                if condition and tg_id in BANNED_USERS:
                    BANNED_USERS.remove(tg_id)
                else:
                    BANNED_USERS.add(tg_id)

                await wrapper.send_message(
                    message.chat.id,
                    plate("user_unbanned") if condition else plate("user_banned"),
                )
                await wrapper.send_message(
                    tg_id,
                    plate("you_are_unbanned") if condition else plate("you_are_banned"),
                )
        else:
            await wrapper.send_message(
                message.chat.id,
                plate("user_not_banned") if condition else plate("user_already_banned"),
            )
    else:
        await wrapper.send_message(
            message.chat.id,
            plate("error") + ":" + plate("id_missing", tg_id=message.command[1]),
        )


@Client.on_message(
    filters.command("busy")
    & ADMINS_FILTER
    & filters.private
    & ~BANNED_USERS
    & ~filters.edited
)
async def busy(_, message):
    if len(message.command) > 1:
        return await wrapper.send_message(
            message.chat.id, plate("no_parameters", command="/busy")
        )

    logging.warning(
        f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /busy"
    )
    if (
        CACHE[message.from_user.id][0] == "IN_CHAT"
        and CACHE[message.from_user.id][1] != 1234567
    ):
        await wrapper.send_message(message.from_user.id, plate("leave_current_chat"))
    elif CACHE[message.from_user.id][0] == "none":
        await wrapper.send_message(message.chat.id, plate("marked_busy"))
        CACHE[message.from_user.id] = ["IN_CHAT", 1234567]
    else:
        if message.from_user.id in CACHE:
            del CACHE[message.from_user.id]
        await wrapper.send_message(message.chat.id, plate("unmarked_busy"))


@Client.on_message(
    filters.command("chats")
    & ADMINS_FILTER
    & filters.private
    & ~BANNED_USERS
    & ~filters.edited
)
async def chats(_, message):
    if len(message.command) > 1:
        return await wrapper.send_message(
            message.chat.id, plate("no_parameters", command="/chats")
        )

    logging.warning(
        f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /chats"
    )
    text = ""
    for user in CACHE:
        if CACHE[user][0] == "IN_CHAT" and user not in ADMINS:
            admin_id = CACHE[user][1]
            admin_name = ADMINS[admin_id]
            text += f"- 👤 [User]({NAME.format(user)}) -> 👨‍💻 [{admin_name}]({NAME.format(admin_id)})\n"
    await wrapper.send_message(message.chat.id, plate("chats_list", chats=text))


@Client.on_message(
    filters.command("queue")
    & ADMINS_FILTER
    & filters.private
    & ~BANNED_USERS
    & ~filters.edited
)
async def queue(_, message):
    if len(message.command) > 1:
        return await wrapper.send_message(
            message.chat.id, plate("no_parameters", command="/queue")
        )

    logging.warning(
        f"{ADMINS[message.from_user.id]} [{message.from_user.id}] sent /queue"
    )
    text = ""
    for user in CACHE:
        if CACHE[user][0] == "AWAITING_ADMIN":
            text += f"- 👤 [User]({NAME.format(user)})\n"
    await wrapper.send_message(message.chat.id, plate("queue_list", queue=text))
