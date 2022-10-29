from rest_framework import serializers
from .models import City

class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= City
        fields = ['city_id', 'name']
