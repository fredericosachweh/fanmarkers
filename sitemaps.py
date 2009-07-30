from django.contrib.sitemaps import Sitemap
from aircraft.models import Aircraft
from main.models import Position, Company
from airport.models import Airport

class AircraftSitemap(Sitemap):

    changefreq = "daily"

    def items(self):
        return Aircraft.objects.all()


class PositionSitemap(Sitemap):

    changefreq = "daily"

    def items(self):
        return Position.objects.all()

    def lastmod(self, obj):
        return obj.last_modified

class CompanySitemap(Sitemap):

    changefreq = "daily"

    def items(self):
        return Company.objects.all()
    
    def lastmod(self, obj):
        return obj.last_modified

class AirportSitemap(Sitemap):

    changefreq="daily"

    def items(self):
        return Airport.relevant.all()

