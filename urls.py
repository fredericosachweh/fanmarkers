from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.contrib import admin
from main.models import *
admin.autodiscover()

company_info = {
    'queryset': Company.objects.all(),
    'template_name': '../templates/list/company.html',
    'template_object_name': 'company',
}

urlpatterns = patterns('',

	(r'^overlay_(?P<z>\d{1,2})_(?P<x>\d{1,5})_(?P<y>\d{1,5})_(?P<o>\S{1,5})/$',		"jobmap.main.views.overlay"),
	
	('^$', 								"jobmap.main.views.jobmap"),

	(r'^site-media/(?P<path>.*)$',					'django.views.static.serve', {'document_root': '/home/chris/Websites/jobmap/media', 'show_indexes': True}),
	(r'^admin/doc/',						include('django.contrib.admindocs.urls')),
	(r'^admin/(.*)',						admin.site.root),
	(r'^comments/',							include('django.contrib.comments.urls')),
	(r'^accounts/',							include('registration.urls')),
	(r'^company/$',							list_detail.object_list, company_info),
	
	(r'^jobmap/',							"jobmap.main.views.jobmap"),
	(r'^position/(?P<pk>\d{1,4})/$',				"jobmap.main.views.position"),
	(r'^company/(?P<pk>\d{1,4})/$',					"jobmap.main.views.company"),
	(r'^airport/(?P<pk>\S{1,7})/$',					"jobmap.main.views.airport"),
	
	(r'^edit/company/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_company"),
	(r'^edit/operation/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_operation"),
	(r'^edit/position/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_position"),
	(r'^edit/route/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_route"),
	
	(r'^new/company/$',						"jobmap.main.views.new_company"),
	(r'^new/operation/(?P<pk>\d{1,4})/$',				"jobmap.main.views.new_operation"),
	(r'^new/position/(?P<pk>\d{1,4})/$',				"jobmap.main.views.new_position"),
	(r'^new/route/(?P<pk>\d{1,4})/$',				"jobmap.main.views.new_route"),
)
