from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Caserne, Region, Tampon, ZoneDesservie, ZoneNonDesservie
from .serializers import (
    CaserneSerializer,
    RegionSerializer,
    TamponSerializer,
    ZoneDesservieSerializer,
    ZoneNonDesservieSerializer,
    CaserneProchSerializer,
    StatsSerializer,
)


class CaserneViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Caserne.objects.all()
    serializer_class = CaserneSerializer

    @action(detail=False, methods=['get'], url_path='proche')
    def caserne_proche(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')

        if not lat or not lng:
            return Response(
                {'erreur': 'Les paramètres lat et lng sont requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            lat = float(lat)
            lng = float(lng)
        except ValueError:
            return Response(
                {'erreur': 'lat et lng doivent être des nombres'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Le point vient en WGS84 (4326) depuis le frontend
        # On le transforme en EPSG:32628 pour calculer la distance en mètres
        point = Point(lng, lat, srid=4326)
        point.transform(32628)

        casernes = Caserne.objects.annotate(
            distance_metres=Distance('geom', point)
        ).order_by('distance_metres')[:5]

        serializer = CaserneProchSerializer(casernes, many=True)
        return Response(serializer.data)


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class TamponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tampon.objects.all()
    serializer_class = TamponSerializer


class ZoneDesservieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ZoneDesservie.objects.all()
    serializer_class = ZoneDesservieSerializer


class ZoneNonDesservieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ZoneNonDesservie.objects.all()
    serializer_class = ZoneNonDesservieSerializer


class StatsViewSet(viewsets.ViewSet):

    def list(self, request):
        population_desservie = 5557860
        population_non_desservie = 11144700
        population_totale = population_desservie + population_non_desservie

        superficie_desservie = 1262.42
        superficie_non_desservie = 195581.0
        superficie_totale = superficie_desservie + superficie_non_desservie

        nombre_casernes = Caserne.objects.count()

        stats = {
            'population_desservie': population_desservie,
            'population_non_desservie': population_non_desservie,
            'population_totale': population_totale,
            'pourcentage_desservi': round(
                population_desservie / population_totale * 100, 1
            ),
            'pourcentage_non_desservi': round(
                population_non_desservie / population_totale * 100, 1
            ),
            'superficie_desservie_km2': superficie_desservie,
            'superficie_non_desservie_km2': superficie_non_desservie,
            'superficie_totale_km2': superficie_totale,
            'pourcentage_superficie_desservie': round(
                superficie_desservie / superficie_totale * 100, 1
            ),
            'nombre_casernes': nombre_casernes,
        }

        serializer = StatsSerializer(stats)
        return Response(serializer.data)