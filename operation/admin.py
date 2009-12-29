from django.contrib import admin
from models import *

class OpBaseInline(admin.TabularInline):
    model = OpBase
    extra = 3
    raw_id_fields = ('base',)


######################################################################

class OperationAdmin(admin.ModelAdmin):
    inlines = (OpBaseInline, )
    list_display = ('company', 'all_fleet', 'all_bases')

class OpBaseAdmin(admin.ModelAdmin):
    raw_id_fields = ('base', )



admin.site.register(OpBase, OpBaseAdmin)
admin.site.register(Operation, OperationAdmin)
