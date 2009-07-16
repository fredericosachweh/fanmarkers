from django.contrib.gis import admin
from models import Aircraft

class AircraftAdmin(admin.ModelAdmin):
	list_display = ('type', 'manufacturer', 'model', 'extra', 'cat_class', 'engine_type',)
	search_fields = ('type', 'model',)
	
admin.site.register(Aircraft, AircraftAdmin)
