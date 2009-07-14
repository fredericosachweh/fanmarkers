from django.conf.urls.defaults import *

urlpatterns = patterns('mins',
	url(r'^(?P<pk>\d{1,4})/$',		"views.edit", name="edit-mins"),
)
