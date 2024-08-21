import aiohttp
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from drfasyncview import AsyncAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.weather.services import WeatherService
from apps.weather.serializers import FilterWeatherSerializer, ResponseSerializer
from apps.weather.fixtures import RESPONSE_FIXTURE





class ListWeatherConditions(AsyncAPIView):

    @swagger_auto_schema(
            operation_description="Retrieve the next 7 days weather conditions of a city",
            query_serializer=FilterWeatherSerializer,
            responses={
                400:openapi.Response(
                    description="Parameter invalid",
                    examples={
                        "application/json": {
                            "city": ["This field is required."]
                        }
                    }
                ),
                503:openapi.Response(
                    description="Error to connect with the city service",
                    examples={
                        "application/json": {
                            "message": "Error to fetch cities"
                        }
                    }
                ),
                200:openapi.Response(
                description="Weather conditions from the query result",
                examples={
                    "application/json": RESPONSE_FIXTURE
                }
                )
            }
            )
    async def get(self, request):
        try:
            paremeters = FilterWeatherSerializer(data=request.query_params)
            paremeters.is_valid(raise_exception=True)
            city = paremeters.data.get('city')
            weather_instance = WeatherService(city_name=city)

            weather_data = await weather_instance.fetch_weather_conditions()

            return Response(status=status.HTTP_200_OK, data=ResponseSerializer(weather_data, many=True).data)
        except aiohttp.ClientError as error:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE, data={'message':str(error)})
        except ValidationError as validation:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=validation.detail)


