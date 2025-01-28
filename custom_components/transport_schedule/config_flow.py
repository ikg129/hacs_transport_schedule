from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_STOP_ID,
    CONF_TRANSPORT_TYPE,
    CONF_WALKING_TIME,
    TRANSPORT_TYPES,
    DEFAULT_TRANSPORT_TYPE,
    DEFAULT_WALKING_TIME,
)

class TransportScheduleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Transport Schedule."""
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            # Walidacja danych
            if len(user_input[CONF_API_KEY]) != 32:
                errors["base"] = "invalid_api_key"
            elif not user_input[CONF_STOP_ID].isdigit():
                errors["base"] = "invalid_stop_id"
            else:
                return self.async_create_entry(
                    title=f"Stop {user_input[CONF_STOP_ID]}", 
                    data=user_input
                )

        schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
            vol.Required(CONF_STOP_ID): str,
            vol.Optional(
                CONF_TRANSPORT_TYPE, 
                default=DEFAULT_TRANSPORT_TYPE
            ): vol.In(TRANSPORT_TYPES),
            vol.Optional(
                CONF_WALKING_TIME, 
                default=DEFAULT_WALKING_TIME
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=30))
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )