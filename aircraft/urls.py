from django.conf.urls.defaults import *
from django.views.generic import create_update
#from forms import AircraftForm

urlpatterns = patterns('aircraft',
        url(r'^$',                                        "views.make_list", name="list-aircraft"),
        url(r'^(?P<pk>\d*)-(?P<slug>[a-z0-9\-]*).html$',  "views.view", name="view-aircraft"),
        url(r'^new/$',                                    "views.new", name="new-aircraft"),
        url(r'^edit/(?P<pk>\d{1,4})/$',                   "views.edit", name="edit-aircraft"),
)
