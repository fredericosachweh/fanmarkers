from django.contrib import admin
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

class CatClassInline(admin.TabularInline):
    model = MinsCatClass
    extra = 3

class OnTypeInline(admin.TabularInline):
    model = MinsOnType
    extra = 1

class PayScaleInline(admin.TabularInline):
    model = PayscaleYear
    extra = 10
######################################################################

class CompanyAdmin(admin.ModelAdmin):
    inlines = (FleetInline, OperationInline, PositionInline)

class CompAdmin(admin.ModelAdmin):
    inlines = (PayScaleInline,)

class OperationAdmin(admin.ModelAdmin):
    inlines = (OpBaseInline, )
    list_display = ('company', 'all_fleet', 'all_bases')

class OpBaseAdmin(admin.ModelAdmin):
    raw_id_fields = ('base', )

class StatusAdmin(admin.ModelAdmin):
    raw_id_fields = ('assign_bases','choice_bases','layoff_bases', )
    #inlines = (StatusBaseInline, )

class PositionAdmin(admin.ModelAdmin):
    pass
    #inlines = (PayScaleInline, )

class MinsAdmin(admin.ModelAdmin):
    inlines = (CatClassInline, OnTypeInline)


admin.site.register(Position,           PositionAdmin)
admin.site.register(Compensation,       CompAdmin)

admin.site.register(OpBase,             OpBaseAdmin)
admin.site.register(Operation,          OperationAdmin)
admin.site.register(Fleet,              )
admin.site.register(Mins,               MinsAdmin)
admin.site.register(MinsCatClass,       )
admin.site.register(MinsOnType,         )
admin.site.register(Company,            CompanyAdmin)
admin.site.register(Status,             StatusAdmin)
