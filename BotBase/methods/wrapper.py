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
from typing import Union

from pyrogram import Client
from pyrogram.errors import RPCError
from pyrogram.types import CallbackQuery, InlineQuery


class MethodWrapper(object):
    """A class that implements a wrapper around ``pyrogram.Client`` methods.
    To access a pyrogram method just call ``MethodWrapper.method_name``.
    All method calls are performed in a try/except block and either return
    the exception object if an error occurs, or the result of the called
    method otherwise. All errors are automatically logged to stderr.

    :param instance: The ``pyrogram.Client`` or ``pyrogram.CallbackQuery`` or ``pyrogram.InlineQuery`` instance (not class!)
    :type instance: Union[Client, CallbackQuery, InlineQuery]
    """

    def __init__(self, instance: Union[Client, CallbackQuery, InlineQuery]):
        """Object constructor"""

        # noinspection PyTypeChecker
        self.instance = instance

    def __getattr__(self, attribute: str):
        if attribute in self.__dict__:
            return self.__dict__[attribute]
        else:

            async def wrapper(*args, **kwargs):
                if hasattr(self.instance, attribute):
                    try:
                        return await getattr(self.instance, attribute)(*args, **kwargs)
                    except RPCError as rpc_error:
                        logging.error(
                            f"An exception occurred -> {type(rpc_error).__name__}: {rpc_error}"
                        )
                        return rpc_error
                else:
                    raise AttributeError(self.instance, attribute)

            return wrapper
