from django.contrib.gis.db import models
from constants import AIRPORT_TYPE

from django.db.models import Q, permalink
from django.contrib.auth.models import User

class BaseManager(models.GeoManager):
    "all airports which are an opbase"
    def get_query_set(self):
        return super(BaseManager, self).get_query_set()\
                                       .filter(opbase__isnull=False)\
                                       .distinct()

class HiringManager(BaseManager):
    "is a base, and either choice or assign are not null"
    def get_query_set(self):
        return super(BaseManager, self).get_query_set()\
                                       .filter(
                                             Q(opbase__assign__isnull=False)
                                           | Q(opbase__choice__isnull=False))\
                                       .distinct()

class NotHiringManager(BaseManager):
    "is a base, and both choice and assign are null"
    def get_query_set(self):
        return super(BaseManager, self).get_query_set()\
                                       .filter(
                                             Q(opbase__assign__isnull=True)\
                                           & Q(opbase__choice__isnull=True))\
                                       .distinct()

class RouteManager(models.GeoManager):
    "is a routebase, but not an opbase"
    def get_query_set(self):
        return super(RouteManager, self).get_query_set()\
                                        .filter(
                                                 Q(routebase__isnull=False)
                                               & Q(opbase__isnull=True))\
                                        .distinct()

class RelevantManager(models.GeoManager):
    "is an opbase, or a routebase"
    def get_query_set(self):
        return super(RelevantManager, self).get_query_set()\
                                           .filter(
                                                    Q(routebase__isnull=False)
                                                  | Q(opbase__isnull=False))\
                                           .distinct()

class Airport(models.Model):
    identifier      =       models.CharField(max_length=8)

    name            =       models.CharField(max_length=96)
    municipality    =       models.CharField(max_length=60)
    country         =       models.ForeignKey("Country")
    region          =       models.ForeignKey("Region")
    type            =       models.IntegerField(choices=AIRPORT_TYPE)

    elevation       =       models.IntegerField(null=True)
    location        =       models.PointField()

    watchers        =       models.ManyToManyField(User, blank=True, )

    objects         =       models.GeoManager()
    hiring          =       HiringManager()
    base            =       BaseManager()
    not_hiring      =       NotHiringManager()
    route           =       RouteManager()
    relevant        =       RelevantManager()

    class Meta:
        ordering = ["identifier", "country"]
        verbose_name_plural = "Airports"

    @models.permalink
    def get_absolute_url(self):
        return ('view-airport',(), {"ident": self.identifier}, )

    def __unicode__(self):
        return u"%s - %s" % (self.identifier, self.location_summary())

    def display_name(self):
        return " - ".join([self.identifier, self.name])

    def location_summary(self):
        ret = []

        for item in (self.municipality, self.region.name, self.country.name):
            if item and item != "United States" and item != "(unassigned)":
                ret.append(item)

        return ", ".join(ret)

class Region(models.Model):
    code = models.CharField(max_length=48)
    country = models.CharField(max_length=2)
    name = models.CharField(max_length=60)
    
    class Meta:
        verbose_name_plural = "Regions"
        
    def __unicode__(self):
        return "%s" % (self.name)

class Country(models.Model):
    name = models.CharField(max_length=48)
    code = models.CharField(max_length=2, primary_key=True)
    continent = models.CharField(max_length=2)
    
    class Meta:
        verbose_name_plural = "Countries"

    def __unicode__(self):
        return self.name
