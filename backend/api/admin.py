from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from django.contrib.gis.geos import Point
from .models import Caserne, Region, Tampon, ZoneDesservie, ZoneNonDesservie
import pyproj


@admin.register(Caserne)
class CaserneAdmin(admin.ModelAdmin):
    list_display = ['fid', 'name', 'operator', 'addr_city', 'addr_street']
    search_fields = ['name', 'operator', 'addr_city']
    list_filter = ['operator']
    exclude = ['geom']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('ajouter-caserne/', self.admin_site.admin_view(self.ajouter_caserne_view), name='ajouter-caserne'),
        ]
        return custom_urls + urls

    def ajouter_caserne_view(self, request):
        if request.method == 'POST':
            try:
                lat = float(request.POST.get('lat'))
                lng = float(request.POST.get('lng'))
                name = request.POST.get('name', '')
                operator = request.POST.get('operator', '')
                addr_city = request.POST.get('addr_city', '')
                addr_street = request.POST.get('addr_street', '')
                osm_id = request.POST.get('osm_id', '')

                # Convertir WGS84 → EPSG:32628
                transformer = pyproj.Transformer.from_crs(4326, 32628, always_xy=True)
                x, y = transformer.transform(lng, lat)
                point = Point(x, y, srid=32628)

                Caserne.objects.create(
                    osm_id=osm_id or None,
                    name=name or None,
                    operator=operator or None,
                    addr_city=addr_city or None,
                    addr_street=addr_street or None,
                    geom=point,
                )

                messages.success(request, f'Caserne "{name}" ajoutée avec succès.')
                return HttpResponseRedirect('../')

            except Exception as e:
                messages.error(request, f'Erreur : {e}')

        context = {
            **self.admin_site.each_context(request),
            'title': 'Ajouter une caserne',
            'opts': self.model._meta,
        }
        return render(request, 'admin/ajouter_caserne.html', context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['ajouter_caserne_url'] = 'ajouter-caserne/'
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['fid', 'name', 'admin_level']
    search_fields = ['name']
    exclude = ['geom']


@admin.register(ZoneDesservie)
class ZoneDesservieAdmin(admin.ModelAdmin):
    list_display = ['fid', 'name']
    exclude = ['geom']


@admin.register(ZoneNonDesservie)
class ZoneNonDesservieAdmin(admin.ModelAdmin):
    list_display = ['fid', 'name']
    exclude = ['geom']


@admin.register(Tampon)
class TamponAdmin(admin.ModelAdmin):
    list_display = ['fid']
    exclude = ['geom']