from django.contrib import admin
from models import Position, Status

class PositionAdmin(admin.ModelAdmin):
    pass
    #inlines = (PayScaleInline, )

class StatusAdmin(admin.ModelAdmin):
    raw_id_fields = ('assign_bases','choice_bases','layoff_bases', )
    #inlines = (StatusBaseInline, )

admin.site.register(Position, PositionAdmin)
admin.site.register(Status, StatusAdmin)
