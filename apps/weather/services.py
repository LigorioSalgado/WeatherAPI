import asyncio
import aiohttp
from  weatherApi.settings import WEATHER_API_KEY



class WeatherService:

    def __init__(self, city_name):
        self._location_service_api = 'https://search.reservamos.mx/api/v2/places'
        self._weather_service_api = 'https://api.openweathermap.org/data/2.5/onecall'
        self._city_name = city_name
        self._result_cities = None
        self._result_weather = []


    async def _fetch_cities(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._location_service_api, params={'q': self._city_name}) as response :
                if response.status != 201:
                    raise aiohttp.ClientError("Error to fetch cities")
                
                self._result_cities = await response.json()

    async def _fetch_weather_for_city(self, session, city):
        try:
            default_params = {
                'exclude': 'current,minutely,hourly,alerts',
                'units': 'metric',
                'appid': WEATHER_API_KEY,
            }
            lat = city.get('lat')
            lon = city.get('long')
        
            if lat and lon:
                params = {'lat': lat, 'lon': lon, **default_params}
                async with session.get(self._weather_service_api, params=params) as response:
                    if response.status != 200:
                        print(response.status)
                        raise aiohttp.ClientError("Error fetching weather conditions")
                    weather_conditions = await response.json()
                    return {
                        'weather_conditions': weather_conditions['daily'],
                        **city
                    }
            else:
                return {
                    'weather_conditions': [],
                    **city
                }
        except aiohttp.ClientError as error:
            return {**city, weather_conditions: {'message': str(error)}}
        
    async def fetch_weather_conditions(self):
        await self._fetch_cities()

        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_weather_for_city(session, city) for city in self._result_cities if city.get('result_type') == 'city']
            self._result_weather = await asyncio.gather(*tasks)

        return self._result_weather




