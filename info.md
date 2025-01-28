## Transport Schedule Integration

This integration retrieves real-time public transport schedules for buses and trams in Warsaw. Configure it to show upcoming departures for stops near your Home Assistant zones.

### Key Features
- Fetches live data from Warsaw Public Transport API.
- Displays the next three departures for each configured stop.
- Automatically detects Home Assistant zones during setup.

### Installation
- Install via [HACS](https://hacs.xyz/) or manually by copying the `custom_components/transport_schedule` folder to your Home Assistant configuration directory.
- Configure the integration through the Home Assistant UI.

### Configuration Options
- **API Key**: Required to access the Warsaw Public Transport API.
- **Update Interval**: Frequency of updates (default: 15 minutes).

### Links
- [GitHub Repository](https://github.com/ikg129/hacs_transport_schedule)
- [API Documentation](https://api.um.warszawa.pl)