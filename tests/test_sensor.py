from unittest.mock import AsyncMock
import pytest
from custom_components.transport_schedule.sensor import TransportScheduleSensor

@pytest.mark.asyncio
async def test_sensor_update():
    """Test the update method of TransportScheduleSensor."""
    # Mock API with a predefined schedule response
    mock_api = AsyncMock()
    mock_api.fetch_schedule = AsyncMock(return_value=[
        {"line": "123", "time": "10:00"}
    ])
    
    # Initialize the sensor with mock API and configuration
    sensor = TransportScheduleSensor(mock_api, {
        "stop_id": "1234",
        "transport_type": "bus"
    })
    
    # Call the sensor's update method
    await sensor._update_data()

    # Verify the sensor's state
    assert sensor.native_value == 1
    assert "departures" in sensor.extra_state_attributes
    assert sensor.extra_state_attributes["departures"][0]["line"] == "123"
    assert sensor.extra_state_attributes["departures"][0]["time"] == "10:00"