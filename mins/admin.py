from django.contrib import admin
from models import *

class CatClassInline(admin.TabularInline):
    model = MinsCatClass
    extra = 3

class OnTypeInline(admin.TabularInline):
    model = MinsOnType
    extra = 1

class MinsAdmin(admin.ModelAdmin):
    inlines = (CatClassInline, OnTypeInline)   

admin.site.register(Mins, MinsAdmin)
admin.site.register(MinsCatClass)
admin.site.register(MinsOnType)
