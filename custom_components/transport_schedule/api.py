"""Komunikacja z API Warszawskiego Transportu Miejskiego."""
from __future__ import annotations
import aiohttp
from aiohttp.client_exceptions import ClientError
import logging
from typing import Any
import async_timeout

from .const import (
    API_BASE_URL,
    API_ENDPOINT_SCHEDULE,
    API_ENDPOINT_STOPS,
    API_TIMEOUT,
    CONF_API_KEY,
    CONF_STOP_ID,
    CONF_TRANSPORT_TYPE,
    TRANSPORT_TYPE_BUS,
    TRANSPORT_TYPE_TRAM,
    API_DATA_KEY,
    API_STATUS_KEY,
    STOP_ID_REGEX,
)

_LOGGER = logging.getLogger(__name__)

class TransportAPIError(Exception):
    """Klasa wyjątku dla błędów API."""

class TransportAPI:
    """Klasa do obsługi API ZTM Warszawa."""
    def __init__(self, api_key: str, session: aiohttp.ClientSession) -> None:
        self._api_key = api_key
        self._session = session  # Używamy sesji z HA zamiast tworzyć własną

    async def _fetch_data(self, endpoint: str, params: dict) -> dict[str, Any]:
        """Wspólna metoda do wysyłania zapytań do API."""
        url = f"{API_BASE_URL}/{endpoint}"
        params.update({"apikey": self._api_key})

        try:
            async with async_timeout.timeout(API_TIMEOUT):
                response = await self._session.get(url, params=params)
                response.raise_for_status()
                data = await response.json()

                if not data.get(API_STATUS_KEY, False):
                    raise TransportAPIError(f"API error: {data.get('error', 'Unknown')}")

                return data.get(API_DATA_KEY, {})
        except ClientError as err:
            _LOGGER.error("Błąd połączenia: %s", err)
            raise TransportAPIError("Connection error") from err

    async def fetch_schedule(self, stop_id: str, transport_type: str) -> list[dict]:
        """Pobierz rozkład jazdy dla przystanku."""
        if transport_type not in [TRANSPORT_TYPE_BUS, TRANSPORT_TYPE_TRAM]:
            raise ValueError("Nieobsługiwany typ transportu")

        params = {
            "busstopId": stop_id,
            "busstopNr": "01",  # Wymagane przez API ZTM (nr słupka)
            "line": ""  # Opcjonalny filtr linii
        }
        try:
            data = await self._fetch_data(API_ENDPOINT_SCHEDULE, params)
            return self._parse_schedule(data)
        except TransportAPIError as err:
            _LOGGER.error("Nie udało się pobrać rozkładu: %s", err)
            return []

    def _parse_schedule(self, raw_data: dict) -> list[dict]:
        """Przetwórz surowe dane API na format integracji."""
        departures = []
        for item in raw_data.get("values", []):
            departures.append({
                "line": item.get("line"),
                "direction": item.get("direction"),
                "time": item.get("time")
            })
        return departures

    async def fetch_stops(self, transport_type: str) -> list[dict]:
        """Pobierz listę przystanków."""
        params = {"type": transport_type}
        try:
            data = await self._fetch_data(API_ENDPOINT_STOPS, params)
            return self._parse_stops(data)
        except TransportAPIError as err:
            _LOGGER.error("Nie udało się pobrać przystanków: %s", err)
            return []

    def _parse_stops(self, raw_data: dict) -> list[dict]:
        """Przetwórz listę przystanków."""
        return [
            {
                "stop_id": item.get("stopId"),
                "name": item.get("stopDesc"),
                "lat": item.get("stopLat"),
                "lon": item.get("stopLon")
            }
            for item in raw_data
        ]