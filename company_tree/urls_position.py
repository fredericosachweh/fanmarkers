from django.conf.urls.defaults import *

urlpatterns = patterns('company_tree',
	(r'^$',				"views_position.make_list"),
	(r'^(?P<pk>\d{1,4})/$',		"views_position.view"),
	(r'^new/(?P<pk>\d{1,4})/$',	"views_position.new"),
	(r'^edit/(?P<pk>\d{1,4})/$',	"views_position.edit"),
)
