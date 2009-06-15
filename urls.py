from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from django.contrib import admin
from main.models import *
from main.forms import *
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
	(r'^aircraft/(?P<pk>\d{1,5})/$',				"jobmap.main.views.aircraft"),
	
	(r'^edit/company/(?P<object_id>\d{1,4})/$',			create_update.update_object, {"form_class": CompanyForm, "template_name": "edit/edit_company.html"}),
	(r'^edit/operation/(?P<object_id>\d{1,4})/$',			create_update.update_object, {"form_class": OperationForm, "template_name": "edit/edit_operation.html"}),
	(r'^edit/position/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_position"),
	(r'^edit/route/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_route"),
	(r'^edit/fleet/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_fleet"),
	(r'^edit/status/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_status"),
	(r'^edit/mins/hard/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_mins", {"min_type": "Hard"}),
	(r'^edit/mins/pref/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_mins", {"min_type": "Preferred"}),
	
	(r'^new/company/$',						create_update.create_object, {"form_class": CompanyForm, "template_name": "new/new_company.html"}),
	(r'^new/operation/(?P<pk>\d{1,4})/$',				"jobmap.main.views.new_operation"),
	(r'^new/position/(?P<pk>\d{1,4})/$',				"jobmap.main.views.new_position"),
	(r'^new/route/(?P<pk>\d{1,4})/$',				"jobmap.main.views.new_route"),
	(r'^new/fleet/(?P<pk>\d{1,4})/$',				"jobmap.main.views.new_fleet"),
)
