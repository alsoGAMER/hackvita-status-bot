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

from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from BotBase.config import (
    ADMINS,
    BUTTONS,
    CACHE,
    GREET,
    NAME,
    PY_VERSION,
    BOT_VERSION,
    BOTBASE_VERSION,
    bot,
    plate,
)
from BotBase.database.query import get_users, set_user
from BotBase.methods import MethodWrapper
from BotBase.methods.custom_filters import user_banned
from BotBase.modules.antiflood import BANNED_USERS
from BotBase.modules.service_status import *

wrapper = MethodWrapper(bot)


@Client.on_message(
    filters.command("start") & ~BANNED_USERS & filters.private & ~user_banned()
)
async def start_handler(_, update):
    """Simply handles the /start command sending a pre-defined greeting
    and saving new users to the database"""
    update_wrapper = MethodWrapper(update)

    if update.from_user.first_name:
        name = update.from_user.first_name
    elif update.from_user.username:
        name = update.from_user.username
    else:
        name = "Anonymous"
    if update.from_user.id not in itertools.chain(*get_users()):
        logging.warning(
            f"New user detected ({update.from_user.id}), adding to database"
        )
        set_user(
            update.from_user.id,
            update.from_user.username.lower() if update.from_user.username else None,
        )
    if GREET:
        if isinstance(update, Message):
            await update_wrapper.reply(
                text=plate(
                    "greet",
                    mention=f"[{name}](tg://user?id={update.from_user.id})",
                    id=update.from_user.id,
                    username=update.from_user.username,
                    website_status="Online"
                    if await get_website_status()
                    else "Offline",
                    qr_code_api_status="Online"
                    if await get_qr_api_status()
                    else "Offline",
                    api_status="Online" if await get_api_status() else "Offline",
                    api_docs_status="Online"
                    if await get_api_docs_status()
                    else "Offline",
                    internal_api_status="Online"
                    if await get_internal_api_status()
                    else "Offline",
                ),
                reply_markup=BUTTONS,
            )
        elif isinstance(update, CallbackQuery):
            if CACHE[update.from_user.id][0] == "AWAITING_ADMIN":
                data = CACHE[update.from_user.id][-1]

                if isinstance(data, list):
                    for chatid, message_ids in data:
                        await wrapper.delete_messages(chatid, message_ids)

                for admin in ADMINS:
                    await wrapper.send_message(
                        chat_id=admin,
                        text=plate(
                            "user_left_queue",
                            user=f"[{name}]({NAME.format(update.from_user.id)})",
                        ),
                    ),

            await update_wrapper.edit_message_text(
                text=plate(
                    "greet",
                    mention=f"[{name}](tg://user?id={update.from_user.id})",
                    id=update.from_user.id,
                    username=update.from_user.username,
                    website_status="Online"
                    if await get_website_status()
                    else "Offline",
                    qr_code_api_status="Online"
                    if await get_qr_api_status()
                    else "Offline",
                    api_status="Online" if await get_api_status() else "Offline",
                    api_docs_status="Online"
                    if await get_api_docs_status()
                    else "Offline",
                    internal_api_status="Online"
                    if await get_internal_api_status()
                    else "Offline",
                ),
                reply_markup=BUTTONS,
            )

            del CACHE[update.from_user.id]
            await update_wrapper.answer()


@Client.on_callback_query(filters.regex("back_start") & ~BANNED_USERS)
async def cb_start_handler(_, message):
    await start_handler(_, message)


@Client.on_callback_query(filters.regex("bot_about") & ~BANNED_USERS)
async def bot_about_handler(_, query):
    cb_wrapper = MethodWrapper(query)
    await cb_wrapper.edit_message_text(
        text=plate(
            "credits",
            python_version=PY_VERSION,
            botbase_version=BOTBASE_VERSION,
            bot_version=BOT_VERSION,
        ),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(plate("back_button"), "back_start")]]
        ),
    )
    await cb_wrapper.answer()


@Client.on_callback_query(filters.regex("bot_disclaimer") & ~BANNED_USERS)
async def bot_disclaimer_handler(_, query):
    cb_wrapper = MethodWrapper(query)
    await cb_wrapper.edit_message_text(
        text=plate("bot_disclaimer_text"),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(plate("back_button"), "back_start")]]
        ),
    )
    await cb_wrapper.answer()


@Client.on_callback_query(filters.regex("services_status_history") & ~BANNED_USERS)
async def services_status_history_handler(_, query):
    cb_wrapper = MethodWrapper(query)
    await cb_wrapper.edit_message_text(
        text=plate(
            "services_status_history_text",
            website_30d_avg=await get_30d_website_history_ratio(),
            website_30d_avg_symbol="✅"
            if await get_30d_website_history_label()
            else "⚠️",
            qr_code_api_30d_avg=await get_30d_qr_api_history_ratio(),
            qr_code_api_30d_avg_symbol="✅"
            if await get_30d_qr_api_history_ratio()
            else "⚠️",
            api_30d_avg=await get_30d_api_history_ratio(),
            api_30d_avg_symbol="✅" if await get_30d_api_history_label() else "⚠️",
            docs_30d_avg=await get_30d_api_docs_history_ratio(),
            docs_30d_avg_symbol="✅" if await get_30d_api_docs_history_label() else "⚠️",
            internal_api_30d_avg=await get_30d_internal_api_history_ratio(),
            internal_api_30d_avg_symbol="✅"
            if await get_30d_internal_api_history_label()
            else "⚠️",
            website_90d_avg=await get_90d_website_history_ratio(),
            website_90d_avg_symbol="✅"
            if await get_90d_website_history_label()
            else "⚠️",
            qr_code_api_90d_avg=await get_90d_qr_api_history_ratio(),
            qr_code_api_90d_avg_symbol="✅"
            if await get_90d_qr_api_history_ratio()
            else "⚠️",
            api_90d_avg=await get_90d_api_history_ratio(),
            api_90d_avg_symbol="✅" if await get_90d_api_history_label() else "⚠️",
            docs_90d_avg=await get_90d_api_docs_history_ratio(),
            docs_90d_avg_symbol="✅" if await get_90d_api_docs_history_label() else "⚠️",
            internal_api_90d_avg=await get_90d_internal_api_history_ratio(),
            internal_api_90d_avg_symbol="✅"
            if await get_90d_internal_api_history_label()
            else "⚠️",
        ),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(plate("back_button"), "back_start")]]
        ),
    )
    await cb_wrapper.answer()
