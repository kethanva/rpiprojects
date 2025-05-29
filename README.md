# Raspberry Pi Dock Project

This project is designed to create a dock on a Raspberry Pi that displays a calendar with date highlights, the current time, and weather information for Bangalore, including the current temperature.
This is using https://openweathermap.org/api/one-call-3
## Project Structure

```
raspberry-pi-dock
├── src
│   ├── main.py               # Entry point of the application
│   ├── calendar
│   │   └── calendar_display.py # Handles calendar display and date highlighting
│   ├── weather
│   │   └── weather_service.py  # Fetches weather data for Bangalore
│   ├── clock
│   │   └── clock_display.py     # Displays the current time
│   └── utils
│       └── config.py           # Configuration settings
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd raspberry-pi-dock
   ```

2. **Install dependencies:**
   Make sure you have Python and pip installed. Then run:
   ```
   brew install python-tk
   pip3 install -r requirements.txt
   ```

3. **Configure API Keys:**
   Update the `src/utils/config.py` file with your API keys for weather services.

4. **Run the application:**
   Execute the main script to start the dock:
   ```
   python3 src/main.py
   ```

## Venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirments.txt
python3 src/main.py

## Functionality

- **Calendar Display:** The dock will show a calendar with highlighted dates based on events.
- **Current Time:** The current time will be displayed in a user-friendly format.
- **Weather Information:** The dock will fetch and display the current weather and temperature for Bangalore.

## Contributing

Feel free to submit issues or pull requests for improvements and features.