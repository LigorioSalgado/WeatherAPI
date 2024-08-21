from unittest.mock import AsyncMock, patch
import pytest
from aiohttp import ClientError
from rest_framework.test import APIRequestFactory

from apps.weather.fixtures import RESPONSE_FIXTURE
from apps.weather.views import ListWeatherConditions
from apps.weather.services import WeatherService


class MockWeatherService(WeatherService):
    async def fetch_weather_conditions(self):
        return [RESPONSE_FIXTURE]

@pytest.mark.asyncio
async def test_list_weather_conditions_success(monkeypatch):
   
    monkeypatch.setattr('apps.weather.views.WeatherService', MockWeatherService)

    factory = APIRequestFactory()
    request = factory.get('/api/weather/', {'city': 'mexico'})

    view = ListWeatherConditions.as_view()

    response = await view(request)

    assert response.status_code == 200
    assert len(response.data) == 1  

@pytest.mark.asyncio
async def test_list_weather_conditions_client_error(monkeypatch):
    async def mock_fetch_weather_conditions(self):
            raise ClientError("Error to fetch cities")

    monkeypatch.setattr('apps.weather.services.WeatherService.fetch_weather_conditions', mock_fetch_weather_conditions)
    factory = APIRequestFactory()
    request = factory.get('/weather/', {'city': 'mexico'})

    view = ListWeatherConditions.as_view()

    response = await view(request)

    assert response.status_code == 503
    assert response.data == {'message': 'Error to fetch cities'}

@pytest.mark.asyncio
@patch('apps.weather.services.WeatherService')
async def test_list_weather_conditions_validation_error(monkeypatch):
    factory = APIRequestFactory()
    request = factory.get('/weather/', {'city': ''})

    view = ListWeatherConditions.as_view()

    response = await view(request)

    assert response.status_code == 400
    assert 'city' in response.data
