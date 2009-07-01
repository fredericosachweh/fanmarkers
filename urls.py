from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from django.contrib import admin

from main.models import *
from main.forms import *
from main.constants import *

admin.autodiscover()

company_list_all = {
		"queryset": Company.objects.all(),
		"template_name": "list_company.html",
		"template_object_name": "company",
		"extra_context": {"types": BUSINESS_TYPE, "title": "All Companies"}
		}
		
company_list_type = {
		"queryset": Company.objects.all(),
		"template_name": "list_company.html",
		"template_object_name": "company",
		"extra_context": {"types": BUSINESS_TYPE, "title": "All Companies"}
		}

company_view = {
		"queryset": Company.objects.all(),
		"template_name": "view_company.html",
		"template_object_name": "company",
		}
		
position_view = {
		"queryset": Position.objects.all(),
		"template_name": "view_position.html",
		"template_object_name": "position",
		}

urlpatterns = patterns('',

	(r'^overlay/(?P<z>\d{1,2})_(?P<x>\d{1,5})_(?P<y>\d{1,5})_(?P<o>\S{1,5})/$', 'main.views.overlay'),
	(r'^admin/doc/',						include('django.contrib.admindocs.urls')),
	(r'^comments/',							include('django.contrib.comments.urls')),
	(r'^admin/(.*)',						admin.site.root),
	(r'^openid/',							include('django_openid_auth.urls')),
	
	
	(r'^site-media/(?P<path>.*)$',					'django.views.static.serve', {'document_root': '/home/chris/Websites/jobmap/media', 'show_indexes': True}),
	
	(r'^profile/',							"jobmap.main.views.profile"),
	
	(r'^jobmap/',							"jobmap.main.views.jobmap"),
	('^$', 								"jobmap.main.views.jobmap"),
	
	(r'^airport/(?P<pk>\S{1,7})/$',					"jobmap.main.views.airport"),
	(r'^aircraft/(?P<pk>\d{1,5})/$',				"jobmap.main.views.aircraft"),
	
	(r'^position/(?P<pk>\d{1,4})/$',				"jobmap.main.views.view_position"),
	(r'^new/position/(?P<pk>\d{1,4})/$',				"jobmap.main.views.new_position"),
	(r'^edit/position/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_position"),
	
	(r'^company/list/all/',						list_detail.object_list, company_list_all),
	(r'^company/list/type/(?P<object_id>\d{1,4})/$',		list_detail.object_list, company_list_type),
	(r'^company/(?P<object_id>\d{1,4})/$',				list_detail.object_detail, company_view),
	(r'^new/company/$',						create_update.create_object, {"form_class": CompanyForm, "template_name": "new_company.html"}),
	(r'^edit/company/(?P<object_id>\d{1,4})/$',			create_update.update_object, {"form_class": CompanyForm, "template_name": "edit_company.html"}),
	
	(r'^edit/operation/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_operation"),
	(r'^new/operation/(?P<pk>\d{1,4})/$',				"jobmap.main.views.new_operation"),
	
	(r'^edit/route/(?P<pk>\d{1,4})/$',				"jobmap.main.views.handle_route", {"type": "edit"}),
	(r'^new/route/(?P<pk>\d{1,4})/$',				"jobmap.main.views.handle_route", {"type": "new"}),

	(r'^edit/fleet/(?P<object_id>\d{1,4})/$',			create_update.update_object, {"form_class": FleetForm, "template_name": "new-edit_fleet.html", "extra_context": {"type": "edit"}}),
	(r'^new/fleet/(?P<pk>\d{1,4})/$',				"jobmap.main.views.new_fleet"),
	
	(r'^edit/mins/hard/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_mins", {"min_type": "Hard"}),
	(r'^edit/mins/pref/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_mins", {"min_type": "Preferred"}),
)

urlpatterns += patterns('django.contrib.auth',
	(r'^accounts/login/$','views.login', {'template_name': 'admin/login.html'}),
	(r'^accounts/logout/$','views.logout', {"template_name": "view_jobmap.html"}),
)
