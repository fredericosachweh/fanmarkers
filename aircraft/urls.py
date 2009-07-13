from django.conf.urls.defaults import *
from django.views.generic import create_update
from forms import AircraftForm

urlpatterns = patterns('aircraft',
	(r'^(?P<pk>\d{1,5})/$',			"views.aircraft"),
	(r'^new$',				create_update.create_object, {"form_class": AircraftForm, "template_name": "new_aircraft.html"}),
	(r'^edit/(?P<object_id>\d{1,4})/$',	create_update.update_object, {"form_class": AircraftForm, "template_name": "edit_aircraft.html"}),
	(r'^$',					"views.make_list"),
)
