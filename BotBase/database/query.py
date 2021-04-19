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

import MySQLdb

from BotBase.config import DB_URL
from BotBase.database.raw_queries import *


def create_table(query: str):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(
            f"An error has occurred while connecting to database: {connection_error}"
        )
    else:
        try:
            with database:
                database.execute(query)
                DB_URL.commit()
                database.close()
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.info(
                f"An error has occurred while executing CREATE_TABLE: {query_error}"
            )


def get_user(tg_id: int):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(
            f"An error has occurred while connecting to database: {connection_error}"
        )
    else:
        try:
            with database:
                database.execute(DB_GET_USER, (tg_id,))
                return database.fetchone()
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(
                f"An error has occurred while executing DB_GET_USER query: {query_error}"
            )
            return query_error


def get_user_by_name(tg_uname: str):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(
            f"An error has occurred while connecting to database: {connection_error}"
        )
    else:
        try:
            with database:
                database.execute(DB_GET_USER_BY_NAME, (tg_uname,))
                return database.fetchone()
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(
                f"An error has occurred while executing DB_GET_USER_BY_NAME query: {query_error}"
            )
            return query_error


def update_name(tg_id: int, name: str):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(
            f"An error has occurred while connecting to database: {connection_error}"
        )
    else:
        try:
            with database:
                database.execute(DB_UPDATE_NAME, (name, tg_id))
                DB_URL.commit()
            return True
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(
                f"An error has occurred while executing DB_UPDATE_NAME query: {query_error}"
            )
            return query_error


def get_users():
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(
            f"An error has occurred while connecting to database: {connection_error}"
        )
    else:
        try:
            with database:
                database.execute(DB_GET_USERS)
                return database.fetchall()
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(
                f"An error has occurred while executing DB_GET_USERS query: {query_error}"
            )
            return query_error


def set_user(tg_id: int, tg_uname: str):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(
            f"An error has occurred while connecting to database: {connection_error}"
        )
    else:
        try:
            with database:
                database.execute(
                    DB_SET_USER,
                    (tg_id, tg_uname, time.strftime("%d/%m/%Y %T %p"), 0),
                )
                DB_URL.commit()
            return True
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(
                f"An error has occurred while executing DB_SET_USER query: {query_error}"
            )
            return query_error


def ban_user(tg_id: int):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(
            f"An error has occurred while connecting to database: {connection_error}"
        )
    else:
        try:
            with database:
                database.execute(DB_BAN_USER, (tg_id,))
                DB_URL.commit()
            return True
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(
                f"An error has occurred while executing DB_BAN_USER query: {query_error}"
            )
            return query_error


def unban_user(tg_id: int):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(
            f"An error has occurred while connecting to database: {connection_error}"
        )
    else:
        try:
            with database:
                database.execute(DB_UNBAN_USER, (tg_id,))
                DB_URL.commit()
            return True
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(
                f"An error has occurred while executing DB_UNBAN_USER query: {query_error}"
            )
            return query_error


def check_banned(tg_id: int):
    try:
        database = DB_URL.cursor()
    except MySQLdb.DatabaseError as connection_error:
        logging.error(
            f"An error has occurred while connecting to database: {connection_error}"
        )
    else:
        try:
            with database:
                database.execute(DB_CHECK_BANNED, (tg_id,))
                return database.fetchone()
        except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as query_error:
            logging.error(
                f"An error has occurred while executing DB_CHECK_BANNED query: {query_error}"
            )
            return query_error
