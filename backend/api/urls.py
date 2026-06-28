from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CaserneViewSet,
    RegionViewSet,
    TamponViewSet,
    ZoneDesservieViewSet,
    ZoneNonDesservieViewSet,
    StatsViewSet,
    RegionStatsViewSet,
)

router = DefaultRouter()
router.register(r'casernes', CaserneViewSet, basename='casernes')
router.register(r'regions', RegionViewSet, basename='regions')
router.register(r'tampons', TamponViewSet, basename='tampons')
router.register(r'zone-desservie', ZoneDesservieViewSet, basename='zone-desservie')
router.register(r'zone-non-desservie', ZoneNonDesservieViewSet, basename='zone-non-desservie')
router.register(r'stats', StatsViewSet, basename='stats')
router.register(r'region-stats', RegionStatsViewSet, basename='region-stats')

urlpatterns = [
    path('', include(router.urls)),
]