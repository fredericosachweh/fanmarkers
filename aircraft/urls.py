from django.conf.urls.defaults import *
from django.views.generic import create_update
from forms import AircraftForm

urlpatterns = patterns('aircraft',
	url(r'^$',					"views.make_list", name="list-aircraft"),
	url(r'^(?P<pk>\d{1,5})/$',			"views.aircraft", name="view-aircraft"),
	url(r'^new$',					create_update.create_object, {"form_class": AircraftForm, "template_name": "new-edit_aircraft.html"}, name="new-aircraft"),
	url(r'^edit/(?P<object_id>\d{1,4})/$',		create_update.update_object, {"form_class": AircraftForm, "template_name": "new-edit_aircraft.html"}, name="edit-aircraft"),

	
)
