from django.contrib.gis import admin
from main.models import *

class PositionInline(admin.StackedInline):
	model = Position
	extra = 1
	
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
	list_display = ('company', 'all_fleet', 'all_bases')
	
class OpBaseAdmin(admin.ModelAdmin):
	raw_id_fields = ('base', )
	
class HSAdmin(admin.ModelAdmin):	
	pass
	#inlines = (StatusBaseInline, )

class PositionAdmin(admin.ModelAdmin):	
	inlines = (PayScaleInline, )
	
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
admin.site.register(OpBase,		OpBaseAdmin)
admin.site.register(Operation, 		OperationAdmin)
admin.site.register(Fleet,		)
admin.site.register(Aircraft, 		AircraftAdmin)
admin.site.register(Mins,		)
admin.site.register(CatClassMins,	)
admin.site.register(Company, 		CompanyAdmin)
admin.site.register(HiringStatus, 	HSAdmin)
