import pytest
from unittest.mock import AsyncMock
from homeassistant.core import HomeAssistant

@pytest.fixture
def hass() -> HomeAssistant:
    """Provide a mock HomeAssistant instance."""
    mock_hass = AsyncMock(spec=HomeAssistant)
    return mock_hass


@pytest.fixture
def mock_api():
    """Provide a mock API object."""
    api = AsyncMock()
    api.fetch_schedule = AsyncMock(return_value=[
        {"line": "123", "time": "10:00"},
        {"line": "456", "time": "10:15"}
    ])
    return api


@pytest.fixture
def valid_config():
    """Provide a valid configuration for testing."""
    return {
        "api_key": "valid32charactersapikeytest12345678",
        "stop_id": "1234",
        "transport_type": "bus",
        "walking_time": 5,
    }


@pytest.fixture
def invalid_config():
    """Provide an invalid configuration for testing."""
    return {
        "api_key": "invalid_key",
        "stop_id": "1234",
        "transport_type": "bus",
        "walking_time": 5,
    }


@pytest.fixture
def missing_data_config():
    """Provide a configuration with missing required data."""
    return {
        "api_key": "valid32charactersapikeytest12345678",
        # Missing "stop_id"
        "transport_type": "bus",
        "walking_time": 5,
    }