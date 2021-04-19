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

# region CreateTablesQueries
CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
                        tg_id INTEGER(20) PRIMARY KEY NOT NULL,
                        tg_uname VARCHAR(32) UNIQUE NULL DEFAULT 'null',
                        date TEXT NOT NULL,
                        banned TINYINT(1) NOT NULL DEFAULT 0)
            """
# endregion


DB_GET_USERS = "SELECT users.tg_id FROM users"
DB_GET_USER = "SELECT * FROM users WHERE users.tg_id = %s"
DB_SET_USER = (
    "INSERT INTO users (tg_id, tg_uname, date, banned) VALUES (%s, %s, %s, %s)"
)
DB_BAN_USER = "UPDATE users SET users.banned = TRUE WHERE users.tg_id = %s"
DB_UNBAN_USER = "UPDATE users SET users.banned = FALSE WHERE users.tg_id = %s"
DB_CHECK_BANNED = "SELECT users.banned FROM users WHERE users.tg_id = %s"
DB_UPDATE_NAME = "UPDATE users SET users.tg_uname = %s WHERE users.tg_id = %s"
DB_GET_USER_BY_NAME = "SELECT * FROM users WHERE users.tg_uname = %s"
