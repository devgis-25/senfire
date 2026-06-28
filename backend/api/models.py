from django.contrib.gis.db import models


class Caserne(models.Model):
    fid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    operator = models.CharField(max_length=255, blank=True, null=True)
    addr_city = models.CharField(
        max_length=255, blank=True, null=True, db_column='addr:city'
    )
    addr_street = models.CharField(
        max_length=255, blank=True, null=True, db_column='addr:street'
    )
    geom = models.PointField(srid=32628)

    class Meta:
        db_table = 'casernes'
        verbose_name = 'Caserne'
        managed = False
        verbose_name_plural = 'Casernes'

    def __str__(self):
        return self.name or f'Caserne {self.fid}'


class Region(models.Model):
    fid = models.AutoField(primary_key=True)
    osm_id = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    admin_level = models.CharField(max_length=10, blank=True, null=True)
    geom = models.MultiPolygonField(srid=32628)

    class Meta:
        db_table = 'regions'
        verbose_name = 'Région'
        managed = False
        verbose_name_plural = 'Régions'

    def __str__(self):
        return self.name or f'Région {self.osm_id}'


class Tampon(models.Model):
    fid = models.AutoField(primary_key=True)
    geom = models.MultiPolygonField(srid=32628)

    class Meta:
        db_table = 'tampons'
        verbose_name = 'Tampon'
        managed = False
        verbose_name_plural = 'Tampons'

    def __str__(self):
        return f'Tampon {self.fid}'


class ZoneDesservie(models.Model):
    fid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    geom = models.MultiPolygonField(srid=32628)

    class Meta:
        db_table = 'zone_desservie'
        verbose_name = 'Zone desservie'
        managed = False
        verbose_name_plural = 'Zones desservies'

    def __str__(self):
        return self.name or f'Zone desservie {self.fid}'


class ZoneNonDesservie(models.Model):
    fid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    geom = models.MultiPolygonField(srid=32628)

    class Meta:
        db_table = 'zone_non_desservie'
        verbose_name = 'Zone non desservie'
        managed = False
        verbose_name_plural = 'Zones non desservies'

    def __str__(self):
        return self.name or f'Zone non desservie {self.fid}'