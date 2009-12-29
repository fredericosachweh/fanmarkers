from django.contrib import admin
from models import *


class PayScaleInline(admin.TabularInline):
    model = PayscaleYear
    extra = 10
    
class CompAdmin(admin.ModelAdmin):
    inlines = (PayScaleInline,)
    
admin.site.register(Compensation, CompAdmin)
