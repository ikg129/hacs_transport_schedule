"""Transport Schedule integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

# Ustawienie loggera
_LOGGER = logging.getLogger(__name__)

# Domenę integracji (powinna być zgodna z "domain" w manifest.json)
DOMAIN = "transport_schedule"

async def async_setup(hass: HomeAssistant, config: dict):
    """Konfiguracja integracji z poziomu configuration.yaml (jeśli obsługiwana)."""
    _LOGGER.info("Setting up Transport Schedule integration via YAML")
    # Możesz zaimplementować konfigurację z YAML, jeśli jest wymagana
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Konfiguracja integracji przy użyciu interfejsu użytkownika."""
    _LOGGER.info("Setting up Transport Schedule integration via Config Flow")
    # Rejestracja sensorów, serwisów itp.
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Dodaj platformy (np. sensor)
    hass.config_entries.async_setup_platforms(entry, ["sensor"])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Wyładowanie integracji."""
    _LOGGER.info("Unloading Transport Schedule integration")
    if entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)

    # Wyładowanie platform (np. sensor)
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])