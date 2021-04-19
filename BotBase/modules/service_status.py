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

import httpx


async def get_website_status():
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_=1618689069664"
        )
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864216:
                x = monitor
                break
        if x["statusClass"] == "success":
            return True
        else:
            return False
    return False


async def get_api_status():
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_=1618689069664"
        )
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864217:
                x = monitor
                break
        if x["statusClass"] == "success":
            return True
        else:
            return False
    return False


async def get_api_docs_status():
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_=1618689069664"
        )
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864218:
                x = monitor
                break
        if x["statusClass"] == "success":
            return True
        else:
            return False
    return False


async def get_internal_api_status():
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_=1618689069664"
        )
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864219:
                x = monitor
                break
        if x["statusClass"] == "success":
            return True
        else:
            return False
    return False
