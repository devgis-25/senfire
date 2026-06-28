from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance, Transform, Intersection, Area
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Caserne, Region, Tampon, ZoneDesservie, ZoneNonDesservie
from .serializers import (
    CaserneSerializer,
    RegionSerializer,
    RegionStatsSerializer,
    TamponSerializer,
    ZoneDesservieSerializer,
    ZoneNonDesservieSerializer,
    CaserneProchSerializer,
    StatsSerializer,
)

from django.db.models import Count, Q


class CaserneViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CaserneSerializer

    def get_queryset(self):
        return Caserne.objects.all().annotate(geom_4326=Transform('geom', 4326))

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

        import pyproj
        transformer = pyproj.Transformer.from_crs(4326, 32628, always_xy=True)
        x, y = transformer.transform(lng, lat)
        point = Point(x, y, srid=32628)

        casernes = Caserne.objects.annotate(
            distance_metres=Distance('geom', point)
        ).order_by('distance_metres')[:5]

        for caserne in casernes:
            caserne.distance_metres = caserne.distance_metres.m

        serializer = CaserneProchSerializer(casernes, many=True)
        return Response(serializer.data)


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RegionSerializer

    def get_queryset(self):
        return Region.objects.all().annotate(geom_4326=Transform('geom', 4326))


class TamponViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TamponSerializer

    def get_queryset(self):
        return Tampon.objects.all().annotate(geom_4326=Transform('geom', 4326))


class ZoneDesservieViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ZoneDesservieSerializer

    def get_queryset(self):
        return ZoneDesservie.objects.all().annotate(geom_4326=Transform('geom', 4326))


class ZoneNonDesservieViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ZoneNonDesservieSerializer

    def get_queryset(self):
        return ZoneNonDesservie.objects.all().annotate(geom_4326=Transform('geom', 4326))


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
            'pourcentage_desservi': round(population_desservie / population_totale * 100, 1),
            'pourcentage_non_desservi': round(population_non_desservie / population_totale * 100, 1),
            'superficie_desservie_km2': superficie_desservie,
            'superficie_non_desservie_km2': superficie_non_desservie,
            'superficie_totale_km2': superficie_totale,
            'pourcentage_superficie_desservie': round(superficie_desservie / superficie_totale * 100, 1),
            'nombre_casernes': nombre_casernes,
        }

        serializer = StatsSerializer(stats)
        return Response(serializer.data)
    




class RegionStatsViewSet(viewsets.ViewSet):
    
    def list(self, request):
        from django.contrib.gis.db.models.functions import Area, Intersection
        from django.db.models import Count

        regions = Region.objects.all()
        resultats = []

        for region in regions:
            # Nombre de casernes dans cette région
            nb_casernes = Caserne.objects.filter(
                geom__within=region.geom
            ).count()

            # Superficie totale de la région en km²
            superficie_region = region.geom.area / 1e6
            
            if superficie_region < 1:
                continue

            # Intersection entre la zone desservie et cette région
            superficie_couverte = 0
            zones = ZoneDesservie.objects.all()
            for zone in zones:
                if zone.geom.intersects(region.geom):
                    intersection = zone.geom.intersection(region.geom)
                    superficie_couverte += intersection.area / 1e6

            # Pourcentage couvert
            pct_couvert = round(superficie_couverte / superficie_region * 100, 1) if superficie_region > 0 else 0

            # Score de priorité — inverse du pourcentage couvert
            # 100 = région totalement non couverte (urgence maximale)
            # 0 = région totalement couverte
            score_priorite = round(100 - pct_couvert, 1)

            resultats.append({
                'nom': region.name or 'Région inconnue',
                'osm_id': region.osm_id,
                'superficie_km2': round(superficie_region, 2),
                'superficie_couverte_km2': round(superficie_couverte, 2),
                'pourcentage_couvert': pct_couvert,
                'nb_casernes': nb_casernes,
                'score_priorite': score_priorite,
            })

        # Trier par score de priorité décroissant
        resultats.sort(key=lambda x: x['score_priorite'], reverse=True)

        serializer = RegionStatsSerializer(resultats, many=True)
        return Response(serializer.data)   