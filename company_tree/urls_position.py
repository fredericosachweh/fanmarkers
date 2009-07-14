from django.conf.urls.defaults import *

urlpatterns = patterns('company_tree',
	url(r'^$',				"views_position.make_list", name="list-position"),
	url(r'^(?P<pk>\d{1,4})/$',		"views_position.view", name="view-position"),
	url(r'^new/(?P<pk>\d{1,4})/$',		"views_position.new", name="new-position"),
	url(r'^edit/(?P<pk>\d{1,4})/$',		"views_position.edit", name="edit-position"),
)
