from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from .const import (
    DOMAIN,
    ATTR_DEPARTURES,
    ATTR_STOP_NAME,
    ATTR_TRANSPORT_TYPE,
    CONF_STOP_ID,
    CONF_TRANSPORT_TYPE,
    CONF_STOP_NAME,
)

class TransportScheduleSensor(SensorEntity):
    """Represents a transport schedule sensor."""
    _attr_icon = "mdi:bus-clock"
    _attr_should_poll = False

    def __init__(self, api, config_data):
        """Initialize the transport schedule sensor."""
        self._api = api
        self._config_data = config_data
        stop_id = config_data.get(CONF_STOP_ID, "unknown")
        self._attr_name = f"Transport {stop_id}"
        self._attr_unique_id = f"transport_{stop_id}"
        self._attr_extra_state_attributes = {
            ATTR_STOP_NAME: "Ładuję...",
            ATTR_DEPARTURES: [],
            ATTR_TRANSPORT_TYPE: config_data.get(CONF_TRANSPORT_TYPE, "unknown"),
        }
        self._attr_native_value = None

    async def async_added_to_hass(self) -> None:
        """Run when the entity is added to Home Assistant."""
        self.async_on_remove(self.hass.helpers.event.async_track_time_interval(
            self._handle_update, 60  # Update every 60 seconds
        ))
        await self._update_data()

    async def _update_data(self):
        """Fetch new data from API."""
        try:
            departures = await self._api.fetch_schedule(
                self._config_data[CONF_STOP_ID],
                self._config_data[CONF_TRANSPORT_TYPE]
            )
            self._attr_extra_state_attributes.update({
                ATTR_DEPARTURES: departures,
                ATTR_STOP_NAME: self._config_data.get(CONF_STOP_NAME, "Unknown"),
            })
            self._attr_native_value = len(departures)
        except Exception as e:
            self._attr_native_value = None
            self._attr_extra_state_attributes.update({
                "error": str(e),
            })
        
        self.async_write_ha_state()

    @callback
    def _handle_update(self, now=None):
        """Trigger update."""
        self.hass.async_create_task(self._update_data())