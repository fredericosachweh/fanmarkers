from django.conf.urls.defaults import *

urlpatterns = patterns('base',
	(r'^(?P<pk>\S{1,7})/$',		"views.airport"),
)
