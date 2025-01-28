import pytest
from unittest.mock import patch
from custom_components.transport_schedule.config_flow import TransportScheduleConfigFlow
from custom_components.transport_schedule.const import DOMAIN


@pytest.mark.asyncio
async def test_flow_user_step_valid_data(hass):
    """Test user step with valid data."""
    flow = TransportScheduleConfigFlow()
    flow.hass = hass

    # Mock the API validation call
    with patch(
        "custom_components.transport_schedule.api.validate_api_key",
        return_value=True,
    ):
        result = await flow.async_step_user()
        assert result["type"] == "form"
        assert result["step_id"] == "user"

        test_data = {
            "api_key": "valid32charactersapikeytest12345678",
            "stop_id": "1234",
            "transport_type": "bus",
            "walking_time": 5,
        }

        result = await flow.async_step_user(test_data)
        assert result["type"] == "create_entry"
        assert result["title"] == "Transport Schedule"
        assert result["data"] == test_data


@pytest.mark.asyncio
async def test_flow_user_step_invalid_api_key(hass):
    """Test user step with an invalid API key."""
    flow = TransportScheduleConfigFlow()
    flow.hass = hass

    # Mock the API validation call to fail
    with patch(
        "custom_components.transport_schedule.api.validate_api_key",
        side_effect=Exception("Invalid API Key"),
    ):
        result = await flow.async_step_user()
        assert result["type"] == "form"
        assert result["step_id"] == "user"

        test_data = {
            "api_key": "invalid_key",
            "stop_id": "1234",
            "transport_type": "bus",
            "walking_time": 5,
        }

        result = await flow.async_step_user(test_data)
        assert result["type"] == "form"
        assert "errors" in result
        assert result["errors"]["base"] == "invalid_api_key"


@pytest.mark.asyncio
async def test_flow_user_step_missing_data(hass):
    """Test user step with missing data."""
    flow = TransportScheduleConfigFlow()
    flow.hass = hass

    result = await flow.async_step_user()
    assert result["type"] == "form"
    assert result["step_id"] == "user"

    test_data = {
        "api_key": "valid32charactersapikeytest12345678",
        # Missing stop_id
        "transport_type": "bus",
        "walking_time": 5,
    }

    result = await flow.async_step_user(test_data)
    assert result["type"] == "form"
    assert "errors" in result
    assert result["errors"]["base"] == "missing_required_field"