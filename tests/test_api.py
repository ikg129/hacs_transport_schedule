import pytest
from unittest.mock import AsyncMock, patch
from aiohttp import ClientSession
from custom_components.transport_schedule.api import TransportAPI, TransportAPIError


@pytest.fixture
def mock_session():
    """Fixture dla mockowanego `aiohttp.ClientSession`."""
    session = AsyncMock(spec=ClientSession)
    return session


@pytest.fixture
def api(mock_session):
    """Fixture dla instancji `TransportAPI`."""
    return TransportAPI(api_key="test_api_key", session=mock_session)


@pytest.mark.asyncio
async def test_fetch_schedule_success(api, mock_session):
    """Test `fetch_schedule` dla poprawnej odpowiedzi API."""
    mock_response = {
        "status": True,
        "data": {
            "values": [
                {"line": "123", "direction": "Centrum", "time": "10:00"},
                {"line": "456", "direction": "Dworzec", "time": "10:15"}
            ]
        }
    }
    mock_session.get.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response)

    result = await api.fetch_schedule(stop_id="1234", transport_type="bus")

    assert len(result) == 2
    assert result[0]["line"] == "123"
    assert result[0]["direction"] == "Centrum"
    assert result[0]["time"] == "10:00"


@pytest.mark.asyncio
async def test_fetch_schedule_invalid_transport_type(api):
    """Test `fetch_schedule` dla nieobsługiwanego typu transportu."""
    with pytest.raises(ValueError, match="Nieobsługiwany typ transportu"):
        await api.fetch_schedule(stop_id="1234", transport_type="invalid_type")


@pytest.mark.asyncio
async def test_fetch_schedule_api_error(api, mock_session):
    """Test `fetch_schedule` dla błędu w odpowiedzi API."""
    mock_response = {
        "status": False,
        "error": "Invalid stop ID"
    }
    mock_session.get.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response)

    result = await api.fetch_schedule(stop_id="1234", transport_type="bus")

    assert result == []


@pytest.mark.asyncio
async def test_fetch_stops_success(api, mock_session):
    """Test `fetch_stops` dla poprawnej odpowiedzi API."""
    mock_response = {
        "status": True,
        "data": [
            {"stopId": "1234", "stopDesc": "Centrum", "stopLat": 52.2297, "stopLon": 21.0122},
            {"stopId": "5678", "stopDesc": "Dworzec", "stopLat": 52.2300, "stopLon": 21.0100},
        ]
    }
    mock_session.get.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response)

    result = await api.fetch_stops(transport_type="bus")

    assert len(result) == 2
    assert result[0]["stop_id"] == "1234"
    assert result[0]["name"] == "Centrum"
    assert result[0]["lat"] == 52.2297
    assert result[0]["lon"] == 21.0122


@pytest.mark.asyncio
async def test_fetch_stops_api_error(api, mock_session):
    """Test `fetch_stops` dla błędu w odpowiedzi API."""
    mock_response = {
        "status": False,
        "error": "Invalid transport type"
    }
    mock_session.get.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response)

    result = await api.fetch_stops(transport_type="tram")

    assert result == []


@pytest.mark.asyncio
async def test_fetch_data_connection_error(api, mock_session):
    """Test `_fetch_data` dla błędu połączenia."""
    mock_session.get.side_effect = Exception("Connection error")

    with pytest.raises(TransportAPIError, match="Connection error"):
        await api._fetch_data("endpoint", {"param": "value"})


def test_parse_schedule(api):
    """Test `_parse_schedule` dla poprawnych danych."""
    raw_data = {
        "values": [
            {"line": "123", "direction": "Centrum", "time": "10:00"},
            {"line": "456", "direction": "Dworzec", "time": "10:15"}
        ]
    }
    result = api._parse_schedule(raw_data)

    assert len(result) == 2
    assert result[0]["line"] == "123"
    assert result[0]["direction"] == "Centrum"
    assert result[0]["time"] == "10:00"


def test_parse_stops(api):
    """Test `_parse_stops` dla poprawnych danych."""
    raw_data = [
        {"stopId": "1234", "stopDesc": "Centrum", "stopLat": 52.2297, "stopLon": 21.0122},
        {"stopId": "5678", "stopDesc": "Dworzec", "stopLat": 52.2300, "stopLon": 21.0100},
    ]
    result = api._parse_stops(raw_data)

    assert len(result) == 2
    assert result[0]["stop_id"] == "1234"
    assert result[0]["name"] == "Centrum"
    assert result[0]["lat"] == 52.2297
    assert result[0]["lon"] == 21.0122