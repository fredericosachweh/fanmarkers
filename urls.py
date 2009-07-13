from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from django.contrib import admin

from main.models import Company
from main.forms import CompanyForm, FleetForm

admin.autodiscover()

company_view = {
		"queryset": Company.objects.all(),
		"template_name": "view_company.html",
		"template_object_name": "company",
		}
		
urlpatterns = patterns('',

	(r'^overlay/(?P<z>\d{1,2})_(?P<x>\d{1,5})_(?P<y>\d{1,5})_(?P<o>\S{1,5})/$', 'main.views.overlay'),
	(r'^map_click/(?P<z>\d{1,2})_(?P<lat>\-?\d+\.\d*)_(?P<lng>\-?\d+\.\d*)/$',		'main.views.map_click'),
	
	(r'^admin/doc/',						include('django.contrib.admindocs.urls')),
	(r'^comments/',							include('django.contrib.comments.urls')),
	(r'^admin/(.*)',						admin.site.root),
	(r'^openid/',							include('django_openid_auth.urls')),
	
	
	(r'^site-media/(?P<path>.*)$',					'django.views.static.serve', {'document_root': '/home/chris/Websites/jobmap/media', 'show_indexes': True}),
	
	(r'^profile/',							"jobmap.main.views.profile"),
	
	(r'^jobmap/',							"jobmap.main.views.jobmap"),
	('^$',								"jobmap.main.views.jobmap"),
	
	##########################################################################################################################################
	
	(r'^airport/',							include("base.urls")),
	(r'^aircraft/',							include("aircraft.urls")),
	(r'^mins/',							include("mins.urls")),
	
	(r'^position/(?P<pk>\d{1,4})/$',				"jobmap.main.views.view_position"),
	(r'^new/position/(?P<pk>\d{1,4})/$',				"jobmap.main.views.new_position"),
	(r'^edit/position/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_position"),
	
	(r'^company/(?P<object_id>\d{1,4})/$',				list_detail.object_detail, company_view),
	(r'^company/new/$',						create_update.create_object, {"form_class": CompanyForm, "template_name": "new_company.html"}),
	(r'^edit/company/(?P<object_id>\d{1,4})/$',			create_update.update_object, {"form_class": CompanyForm, "template_name": "edit_company.html"}),
	
	###########################################################################################################################################
	
	(r'^edit/operation/(?P<pk>\d{1,4})/$',				"jobmap.main.views.edit_operation"),
	(r'^new/operation/(?P<pk>\d{1,4})/$',				"jobmap.main.views.new_operation"),
	
	(r'^edit/route/(?P<pk>\d{1,4})/$',				"jobmap.main.views.handle_route", {"type": "edit"}),
	(r'^new/route/(?P<pk>\d{1,4})/$',				"jobmap.main.views.handle_route", {"type": "new"}),

	(r'^edit/fleet/(?P<object_id>\d{1,4})/$',			create_update.update_object, {"form_class": FleetForm, "template_name": "new-edit_fleet.html", "extra_context": {"type": "edit"}}),
	(r'^new/fleet/(?P<pk>\d{1,4})/$',				"jobmap.main.views.new_fleet"),
	
	###########################################################################################################################################
	
	(r'^kml/position-(?P<position>\d{1,4}).kml$',			"jobmap.main.views.kml"),
	(r'^kml/company-(?P<company>\d{1,4}).kml$',			"jobmap.main.views.kml"),
	(r'^kml/airport-(?P<airport>[A-Z]{1,5}).kml$',			"jobmap.main.views.kml"),
	
	###########################################################################################################################################
	
	(r'^company/list/$',						"jobmap.main.list_views.company"),
	(r'^position/list/$',						"jobmap.main.list_views.position"),
	
)

urlpatterns += patterns('django.contrib.auth',
	(r'^accounts/logout/$','views.logout', {"template_name": "view_jobmap.html"}),
)
