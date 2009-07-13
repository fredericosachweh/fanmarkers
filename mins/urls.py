from django.conf.urls.defaults import *

urlpatterns = patterns('mins',
	(r'^(?P<pk>\d{1,4})/$',		"views.edit"),
)
