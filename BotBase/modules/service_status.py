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

import httpx
from cachetools import cached, TTLCache

from BotBase.methods.cacheable import cacheable

timestamp = int(time.time() * 1000)


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_website_status():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return False
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


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_30d_website_history_ratio():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return "N/A"
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864216:
                x = monitor
                break
        return x["30dRatio"]["ratio"]


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_90d_website_history_ratio():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return "N/A"
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864216:
                x = monitor
                break
        return x["90dRatio"]["ratio"]


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_30d_website_history_label():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return False
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864216:
                x = monitor
                break
        if not x["30dRatio"]["label"] == "success":
            return False
        else:
            return True


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_90d_website_history_label():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return False
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864216:
                x = monitor
                break
        if not x["90dRatio"]["label"] == "success":
            return False
        else:
            return True


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_api_status():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return False
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


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_30d_api_history_ratio():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return "N/A"
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864217:
                x = monitor
                break
        return x["30dRatio"]["ratio"]


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_90d_api_history_ratio():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return "N/A"
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864217:
                x = monitor
                break
        return x["90dRatio"]["ratio"]


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_30d_api_history_label():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return False
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864217:
                x = monitor
                break
        if not x["30dRatio"]["label"] == "success":
            return False
        else:
            return True


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_90d_api_history_label():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return False
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864217:
                x = monitor
                break
        if not x["90dRatio"]["label"] == "success":
            return False
        else:
            return True


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_api_docs_status():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return False
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


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_30d_api_docs_history_ratio():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return "N/A"
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864218:
                x = monitor
                break
        return x["30dRatio"]["ratio"]


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_90d_api_docs_history_ratio():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return "N/A"
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864218:
                x = monitor
                break
        return x["90dRatio"]["ratio"]


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_30d_api_docs_history_label():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return False
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864218:
                x = monitor
                break
        if not x["30dRatio"]["label"] == "success":
            return False
        else:
            return True


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_90d_api_docs_history_label():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return False
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864218:
                x = monitor
                break
        if not x["90dRatio"]["label"] == "success":
            return False
        else:
            return True


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_internal_api_status():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return False
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


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_30d_internal_api_history_ratio():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return "N/A"
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864219:
                x = monitor
                break
        return x["30dRatio"]["ratio"]


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_90d_internal_api_history_ratio():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return "N/A"
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864219:
                x = monitor
                break
        return x["90dRatio"]["ratio"]


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_30d_internal_api_history_label():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return False
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864219:
                x = monitor
                break
        if not x["30dRatio"]["label"] == "success":
            return False
        else:
            return True


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_90d_internal_api_history_label():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return False
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787864219:
                x = monitor
                break
        if not x["90dRatio"]["label"] == "success":
            return False
        else:
            return True


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_qr_api_status():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return False
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787920021:
                x = monitor
                break
        if x["statusClass"] == "success":
            return True
        else:
            return False
    return False


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_30d_qr_api_history_ratio():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return "N/A"
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787920021:
                x = monitor
                break
        return x["30dRatio"]["ratio"]


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_90d_qr_api_history_ratio():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return "N/A"
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787920021:
                x = monitor
                break
        return x["90dRatio"]["ratio"]


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_30d_qr_api_history_label():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return False
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787920021:
                x = monitor
                break
        if not x["30dRatio"]["label"] == "success":
            return False
        else:
            return True


@cached(cache=TTLCache(maxsize=1, ttl=300))
@cacheable
async def get_90d_qr_api_history_label():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"https://status.hackvita.eu/api/getMonitorList/MW0n9u5897?page=1&_={timestamp}"
            )
        except httpx.HTTPError as e:
            logging.error(f"An error occurred while contacting {e.request.url}: {e}")
            return False
    if r.json()["status"] == "ok":
        x = None
        for monitor in r.json()["psp"]["monitors"]:
            if monitor["monitorId"] == 787920021:
                x = monitor
                break
        if not x["90dRatio"]["label"] == "success":
            return False
        else:
            return True
