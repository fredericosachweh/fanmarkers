from django.contrib.gis import admin
from models import *
from mins import *

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
		
class CatClassInline(admin.TabularInline):
	model = CatClassMins
	extra = 3
	
class OnTypeInline(admin.TabularInline):
	model = OnTypeMins
	extra = 1
	
######################################################################
	
class CompanyAdmin(admin.ModelAdmin):
	inlines = (FleetInline, OperationInline, PositionInline)
	
class RouteAdmin(admin.ModelAdmin):
	inlines = (RouteBaseInline,)

class CompAdmin(admin.ModelAdmin):
	inlines = (PayScaleInline,)

class OperationAdmin(admin.ModelAdmin):
	inlines = (OpBaseInline, )
	list_display = ('company', 'all_fleet', 'all_bases')
	
class OpBaseAdmin(admin.ModelAdmin):
	raw_id_fields = ('base', )
	
class StatusAdmin(admin.ModelAdmin):	
	raw_id_fields = ('assign_bases','choice_bases','layoff_bases','not_bases', )
	#inlines = (StatusBaseInline, )

class PositionAdmin(admin.ModelAdmin):	
	pass
	#inlines = (PayScaleInline, )
	
class MinsAdmin(admin.ModelAdmin):
	inlines = (CatClassInline, OnTypeInline)


admin.site.register(Position,		PositionAdmin)
admin.site.register(Compensation,	CompAdmin)
admin.site.register(Route, 		RouteAdmin)
admin.site.register(RouteBase, 		)
admin.site.register(OpBase,		OpBaseAdmin)
admin.site.register(Operation, 		OperationAdmin)
admin.site.register(Fleet,		)
admin.site.register(Mins,		MinsAdmin)
admin.site.register(CatClassMins,	)
admin.site.register(OnTypeMins,		)
admin.site.register(Company, 		CompanyAdmin)
admin.site.register(Status, 		StatusAdmin)
