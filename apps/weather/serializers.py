from rest_framework import serializers
import datetime 

class FilterWeatherSerializer(serializers.Serializer):
    city = serializers.CharField(min_length=3)
    # we can add further params


class WeatherSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    main = serializers.CharField()
    description = serializers.CharField()
    icon = serializers.CharField()

class TemperatureSerializer(serializers.Serializer):
    day = serializers.FloatField()
    min = serializers.FloatField()
    max = serializers.FloatField()
    night = serializers.FloatField()
    eve = serializers.FloatField()
    morn = serializers.FloatField()

class FeelsLikeSerializer(serializers.Serializer):
    day = serializers.FloatField()
    night = serializers.FloatField()
    eve = serializers.FloatField()
    morn = serializers.FloatField()

class WeatherConditionsSerializer(serializers.Serializer):
    dt = serializers.IntegerField()  
    temp = TemperatureSerializer()
    feels_like = FeelsLikeSerializer()
    weather = WeatherSerializer(many=True)
    iso_date = serializers.SerializerMethodField()

    def iso_date(self,obj):
        return datetime.datetime.fromtimestamp(obj.get('dt'), datetime.timezone.utc)



class ResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    city_name = serializers.CharField(max_length=100)
    city_slug = serializers.CharField(max_length=100)
    result_type = serializers.CharField(max_length=100)
    weather_conditions = WeatherConditionsSerializer(many=True)