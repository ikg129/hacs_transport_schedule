"""Constants for Transport Schedule integration."""
from typing import Final

# Domain
DOMAIN: Final = "transport_schedule"
DEFAULT_SCAN_INTERVAL: Final = 300  # 5 minut (w sekundach)

# API Configuration
API_BASE_URL: Final = "https://api.um.warszawa.pl/api/action"
API_TIMEOUT: Final = 10  # sekundy
USER_AGENT: Final = f"HomeAssistant/{DOMAIN}/1.0"

# Endpoints
API_ENDPOINT_SCHEDULE: Final = "dbtimetable_get"
API_ENDPOINT_STOPS: Final = "dbstore_get"  # Sprawdź dokładną nazwę endpointu w dokumentacji API!

# Configuration Keys
CONF_API_KEY: Final = "api_key"
CONF_STOP_ID: Final = "stop_id"
CONF_STOP_NAME: Final = "stop_name"
CONF_TRANSPORT_TYPE: Final = "transport_type"
CONF_WALKING_TIME: Final = "walking_time"
CONF_UPDATE_INTERVAL: Final = "update_interval"

# Transport Types
TRANSPORT_TYPE_BUS: Final = "bus"
TRANSPORT_TYPE_TRAM: Final = "tram"
TRANSPORT_TYPES: Final = [TRANSPORT_TYPE_BUS, TRANSPORT_TYPE_TRAM]

# Defaults
DEFAULT_TRANSPORT_TYPE: Final = TRANSPORT_TYPE_BUS
DEFAULT_WALKING_TIME: Final = 5  # minuty
DEFAULT_STOP_NAME: Final = "Unknown Stop"

# Attributes
ATTR_STOP_ID: Final = "stop_id"
ATTR_STOP_NAME: Final = "stop_name"
ATTR_DEPARTURES: Final = "departures"
ATTR_TRANSPORT_TYPE: Final = "transport_type"
ATTR_NEXT_ARRIVAL: Final = "next_arrival"  # Dodatkowy przydatny atrybut

# Translation Keys
TRANS_KEY_STOP_ID: Final = "stop_id"
TRANS_KEY_WALKING_TIME: Final = "walking_time"

# Error Handling
API_DATA_KEY: Final = "result"  # Klucz z odpowiedzi API zawierający dane
API_STATUS_KEY: Final = "success"  # Klucz statusu odpowiedzi API
STOP_ID_REGEX: Final = r"^\d{4}$"  # Przykładowy regex dla ID przystanku (dostosuj do rzeczywistych danych)