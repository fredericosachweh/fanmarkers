from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.contrib import admin
from main.models import *
admin.autodiscover()

company_info = {
    'queryset': Company.objects.all(),
    'template_name': '../templates/company_list.html',
    'template_object_name': 'company',
}

urlpatterns = patterns('',
	
	('^$', 									"jobmap.main.views.jobmap"),

	(r'^site-media/(?P<path>.*)$',						'django.views.static.serve', {'document_root': '/home/chris/Websites/jobmap/media', 'show_indexes': True}),
	(r'^admin/doc/',							include('django.contrib.admindocs.urls')),
	(r'^admin/(.*)',							admin.site.root),
	(r'^comments/',								include('django.contrib.comments.urls')),
	(r'^accounts/',								include('registration.urls')),

	(r'^jobmap/',								"jobmap.main.views.jobmap"),
	(r'^company/(?P<company_id>\d{1,4})/$',					"jobmap.main.views.company"),
	(r'^company/$',								list_detail.object_list, company_info),
	
	(r'^edit/company/(?P<company_id>\d{1,4})/$',				"jobmap.main.views.edit_company"),
	(r'^edit/operation/(?P<op_id>\d{1,4})/$',				"jobmap.main.views.edit_operation"),
	
	(r'^base_overlay_(?P<z>\d{1,2})_(?P<x>\d{1,5})_(?P<y>\d{1,5})_(?P<o>\S{1,5})/$',		"jobmap.main.views.base_overlay"),
	(r'^airport/(?P<airport_id>\S{1,7})/$',					"jobmap.main.views.airport"),
)
