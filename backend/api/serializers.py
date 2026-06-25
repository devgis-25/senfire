from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import Caserne, Region, Tampon, ZoneDesservie, ZoneNonDesservie


class CaserneSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Caserne
        geo_field = 'geom'
        fields = [
            'fid',
            'osm_id',
            'name',
            'operator',
            'addr_city',
            'addr_street',
        ]


class RegionSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Region
        geo_field = 'geom'
        fields = [
            'fid',
            'osm_id',
            'name',
            'admin_level',
        ]


class TamponSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Tampon
        geo_field = 'geom'
        fields = ['fid']


class ZoneDesservieSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ZoneDesservie
        geo_field = 'geom'
        fields = [
            'fid',
            'name',
        ]


class ZoneNonDesservieSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ZoneNonDesservie
        geo_field = 'geom'
        fields = [
            'fid',
            'name',
        ]


class CaserneProchSerializer(serializers.ModelSerializer):
    distance_metres = serializers.FloatField()
    distance_km = serializers.SerializerMethodField()

    class Meta:
        model = Caserne
        fields = [
            'fid',
            'name',
            'operator',
            'addr_city',
            'distance_metres',
            'distance_km',
        ]

    def get_distance_km(self, obj):
        return round(obj.distance_metres / 1000, 2)


class StatsSerializer(serializers.Serializer):
    population_desservie = serializers.IntegerField()
    population_non_desservie = serializers.IntegerField()
    population_totale = serializers.IntegerField()
    pourcentage_desservi = serializers.FloatField()
    pourcentage_non_desservi = serializers.FloatField()
    superficie_desservie_km2 = serializers.FloatField()
    superficie_non_desservie_km2 = serializers.FloatField()
    superficie_totale_km2 = serializers.FloatField()
    pourcentage_superficie_desservie = serializers.FloatField()
    nombre_casernes = serializers.IntegerField()