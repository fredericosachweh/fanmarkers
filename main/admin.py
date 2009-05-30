from django.contrib.gis import admin
from main.models import *

class PositionInline(admin.StackedInline):
	model = Position
	extra = 1
	raw_id_fields = ('hiring_possible','hiring_direct')
	
class FleetInline(admin.TabularInline):
	model = Fleet
	extra = 3
	
class OperationInline(admin.TabularInline):
	model = Operation
	extra = 3
	
class OpBaseInline(admin.TabularInline):
	model = OpBase
	extra = 3
	raw_id_fields = ('base',)
	
class PayScaleInline(admin.TabularInline):
	model = PayscaleYear
	extra = 10
	
class RouteBaseInline(admin.TabularInline):
	model = RouteBase
	extra = 3
	raw_id_fields = ('base',)
######################################################################
	
class CompanyAdmin(admin.ModelAdmin):
	inlines = (FleetInline, OperationInline, PositionInline)
	
class RouteAdmin(admin.ModelAdmin):
	inlines = (RouteBaseInline,)

class OperationAdmin(admin.ModelAdmin):
	inlines = (OpBaseInline, )
	
class PositionAdmin(admin.ModelAdmin):	
	raw_id_fields = ('hiring_possible','hiring_direct')
	inlines = (PayScaleInline,)
	
class BaseAdmin(admin.GeoModelAdmin):
	list_display = ('identifier', 'name', 'country', 'region', 'municipality',)
	search_fields = ('identifier', 'name', 'municipality',)
	
class AircraftAdmin(admin.ModelAdmin):
	list_display = ('type', 'manufacturer', 'model', 'extra', 'cat_class', 'engine_type',)
	search_fields = ('type', 'model',)


admin.site.register(Position,		PositionAdmin)
admin.site.register(Route, 		RouteAdmin)
admin.site.register(Base, 		BaseAdmin)
admin.site.register(RouteBase, 		)
admin.site.register(OpBase		)
admin.site.register(Operation, 		OperationAdmin)
admin.site.register(Fleet,		)
admin.site.register(Aircraft, 		AircraftAdmin)
admin.site.register(Mins,		)
admin.site.register(Company, 		CompanyAdmin)
