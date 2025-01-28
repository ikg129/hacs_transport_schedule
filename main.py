from custom_components.transport_schedule.api import TransportAPI
from custom_components.transport_schedule.const import DOMAIN, DEFAULT_UPDATE_INTERVAL
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.components.sensor import SensorEntity

import logging
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Set up the integration from YAML configuration."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass, config_entry):
    """Set up the integration from a config entry."""
    api_key = config_entry.data[CONF_API_KEY]
    update_interval = timedelta(seconds=config_entry.data.get("update_interval", DEFAULT_UPDATE_INTERVAL))

    api = TransportAPI(api_key, hass.helpers.aiohttp_client.async_get_clientsession(hass))
    coordinator = TransportDataCoordinator(hass, api, update_interval)

    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    # Perform the first update
    await coordinator.async_config_entry_first_refresh()

    # Set up platforms (sensors)
    hass.config_entries.async_setup_platforms(config_entry, ["sensor"])

    return True

class TransportDataCoordinator(DataUpdateCoordinator):
    """Coordinator to manage data updates from the API."""

    def __init__(self, hass, api, update_interval):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.api = api
        self.sensors = []

    async def _async_update_data(self):
        """Fetch the latest data from the API."""
        data = {}
        for sensor in self.sensors:
            try:
                schedule = await self.api.fetch_schedule(sensor.stop_id, sensor.transport_type)
                data[sensor.stop_id] = schedule
            except Exception as err:
                _LOGGER.error("Error fetching data for stop %s: %s", sensor.stop_id, err)
                raise UpdateFailed(f"Error fetching data: {err}")
        return data

class TransportScheduleSensor(SensorEntity):
    """Sensor to represent a single transport schedule."""

    def __init__(self, coordinator, stop_id, transport_type, name):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self.stop_id = stop_id
        self.transport_type = transport_type
        self._attr_name = name

    @property
    def native_value(self):
        """Return the next departure time."""
        data = self.coordinator.data.get(self.stop_id, [])
        return len(data)  # Number of departures

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        data = self.coordinator.data.get(self.stop_id, [])
        return {
            "departures": data[:3]  # Limit to the next 3 departures
        }
