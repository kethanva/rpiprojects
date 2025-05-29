class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall"
        self.lat = "12.9406"
        self.lon = "77.5738"
    def fetch_weather(self):
        import requests
        params = {
            'lat': self.lat,
            'lon': self.lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_temperature(self):
        weather_data = self.fetch_weather()
        if weather_data and 'main' in weather_data:
            return weather_data['main']['temp']
        return None