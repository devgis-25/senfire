from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.fields import GeometryField
from rest_framework import serializers
from .models import Caserne, Region, Tampon, ZoneDesservie, ZoneNonDesservie


class CaserneSerializer(GeoFeatureModelSerializer):
    geom_4326 = GeometryField()

    class Meta:
        model = Caserne
        geo_field = 'geom_4326'
        fields = ['fid', 'osm_id', 'name', 'operator', 'addr_city', 'addr_street', 'geom_4326']


class RegionSerializer(GeoFeatureModelSerializer):
    geom_4326 = GeometryField()

    class Meta:
        model = Region
        geo_field = 'geom_4326'
        fields = ['fid', 'osm_id', 'name', 'admin_level', 'geom_4326']


class TamponSerializer(GeoFeatureModelSerializer):
    geom_4326 = GeometryField()

    class Meta:
        model = Tampon
        geo_field = 'geom_4326'
        fields = ['fid', 'geom_4326']


class ZoneDesservieSerializer(GeoFeatureModelSerializer):
    geom_4326 = GeometryField()

    class Meta:
        model = ZoneDesservie
        geo_field = 'geom_4326'
        fields = ['fid', 'name', 'geom_4326']


class ZoneNonDesservieSerializer(GeoFeatureModelSerializer):
    geom_4326 = GeometryField()

    class Meta:
        model = ZoneNonDesservie
        geo_field = 'geom_4326'
        fields = ['fid', 'name', 'geom_4326']


class CaserneProchSerializer(serializers.ModelSerializer):
    distance_metres = serializers.FloatField()
    distance_km = serializers.SerializerMethodField()

    class Meta:
        model = Caserne
        fields = ['fid', 'name', 'operator', 'addr_city', 'distance_metres', 'distance_km']

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
    
    

class RegionStatsSerializer(serializers.Serializer):
    nom = serializers.CharField()
    osm_id = serializers.CharField()
    superficie_km2 = serializers.FloatField()
    superficie_couverte_km2 = serializers.FloatField()
    pourcentage_couvert = serializers.FloatField()
    nb_casernes = serializers.IntegerField()
    score_priorite = serializers.FloatField()    