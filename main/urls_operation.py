from django.conf.urls.defaults import *

urlpatterns = patterns('main',
	url(r'^new/(?P<pk>\d{1,4})/$',		"views_operation.new", name="new-operation"),
	url(r'^edit/(?P<pk>\d{1,4})/$',		"views_operation.edit", name="edit-operation"),
)
