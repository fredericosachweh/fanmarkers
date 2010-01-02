from django.contrib.gis import admin
from models import Airport, Country, Region

class AirportAdmin(admin.GeoModelAdmin):
    list_display = ('identifier', 'name', 'country', 'region', 'municipality',)
    search_fields = ('identifier', 'name', 'municipality',)

admin.site.register(Airport, AirportAdmin)
admin.site.register(Country)
admin.site.register(Region)
