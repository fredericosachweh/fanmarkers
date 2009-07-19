from django.contrib import admin
from models import *

class RouteBaseInline(admin.TabularInline):
    model = RouteBase
    extra = 3
    raw_id_fields = ('base',)

class RouteAdmin(admin.ModelAdmin):
    inlines = (RouteBaseInline,)

admin.site.register(Route, RouteAdmin)
admin.site.register(RouteBase)
