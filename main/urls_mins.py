from django.conf.urls.defaults import *

urlpatterns = patterns('main',
	url(r'^(?P<pk>\d{1,4})/$',		"views_mins.edit", name="edit-mins"),
)
