from django.conf.urls.defaults import *

urlpatterns = patterns('main',
	url(r'^new/(?P<pk>\d{1,4})/$',		"views_fleet.new", name="new-fleet"),
	url(r'^edit/(?P<pk>\d{1,4})/$',		"views_fleet.edit", name="edit-fleet"),
)
