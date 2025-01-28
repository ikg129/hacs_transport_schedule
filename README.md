# hacs_transport_schedule
HACS add-on for Home Assistant providing bus and tram timetables based on the location nearest to HA

# HACS Transport Schedule Integration

[![HACS Integration](https://img.shields.io/badge/HACS-Custom-blue.svg)](https://hacs.xyz/)

This Home Assistant integration provides real-time bus and tram schedules for the nearest public transport stops based on your Home Assistant zones and configured locations. Data is retrieved from the [Warsaw Public Transport API (CKAN)](https://api.um.warszawa.pl/#).

## Features

- Displays the next three departures for each configured stop.
- Automatically detects Home Assistant zones for initial setup.
- Customizable update intervals (default: 15 minutes).
- Supports configuration through the Home Assistant UI or YAML.

## Installation

### Using HACS
1. Add this repository to HACS as a custom repository:
   - Go to **HACS > Integrations > Add Repository**.
   - Paste the repository URL: `https://github.com/ikg129/hacs_transport_schedule`.
2. Install the integration.
3. Restart Home Assistant.

### Manual Installation
1. Clone or download this repository.
2. Copy the `custom_components/transport_schedule` directory to your Home Assistant `config/custom_components` folder.
3. Restart Home Assistant.

## Configuration

### Using the UI
1. Go to **Settings > Integrations > Add Integration**.
2. Search for **Transport Schedule** and select it.
3. Configure the API key and other settings.

### YAML Configuration (Optional)
Add the following to your `configuration.yaml`:
```yaml
transport_schedule:
  api_key: YOUR_API_KEY
  update_interval: 900  # Optional: update interval in seconds (default: 900)

Example Use Cases
	•	Display upcoming departures for your nearest bus or tram stop.
	•	Configure multiple stops based on your Home Assistant zones.

Troubleshooting
	•	Ensure your API key from the Warsaw Public Transport API is valid.
	•	Check Home Assistant logs for detailed error messages.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Contributing

Contributions are welcome! Please open an issue or pull request on GitHub.

  # location Poland, area Warsaw, bellow regulation for usage of public data (in Polish)
Dane publiczne dostępne w serwisie są materiałami urzędowymi i jako takie nie są chronione przez prawa autorskie. Dodatkowo, większość surowych danych nie ma charakteru twórczego i jako takie też nie są chronione przez prawo autorskie. Oznacza to, że z danych tych można swobodnie korzystać. Należy jedynie przestrzegać warunków ponownego wykorzystywania informacji publicznej, wynikających z ustawy o ponownym wykorzystywaniu informacji sektora publicznego z 25 lutego 2016 r.

źródło danych : Miasto Stołeczne Warszawa oraz, 
serwis otwarte dane po warszawsku: http://api.um.warszawa.pl
data wytworzenia oraz pozyskania informacji publicznej 29.01.2025
Ponowne wykorzystanie informacji sektora publicznego dostępnych w serwisie następuje na własną odpowiedzialność wnioskodawcy. Miasto Stołeczne Warszawa nie ponosi odpowiedzialności za ewentualną szkodę wynikającą z ponownego wykorzystania tych informacji przez wnioskodawcę lub innych użytkowników. Miasto Stołeczne Warszawa zastrzega, że niektóre z ponownie wykorzystywanych informacji przetworzonych przez osoby trzecie mogą być nieaktualne lub zawierać błędy.