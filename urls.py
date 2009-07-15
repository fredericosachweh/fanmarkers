from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from django.contrib import admin

###############################################
#from django.db.models.loading import cache as model_cache
#if not model_cache.loaded:
#	model_cache.get_models()
#admin.autodiscover()
##############################################

urlpatterns = patterns('',

	(r'^overlay/(?P<z>\d{1,2})_(?P<x>\d{1,5})_(?P<y>\d{1,5})_(?P<o>\S{1,5})/$',
									'company_tree.views_map.overlay'),
		    
	(r'^map_click/(?P<z>\d{1,2})_(?P<lat>\-?\d+\.\d*)_(?P<lng>\-?\d+\.\d*)/$',
									'company_tree.views_map.click'),
	
	(r'^admin/doc/',				include('django.contrib.admindocs.urls')),
	(r'^comments/',					include('django.contrib.comments.urls')),
	(r'^admin/(.*)',				admin.site.root),
	(r'^openid/',					include('django_openid_auth.urls')),
	
	
	(r'^site-media/(?P<path>.*)$',			'django.views.static.serve', {'document_root': '/home/chris/Websites/jobmap/media', 'show_indexes': True}),
	
	#(r'^profile/',					"company_tree.views.profile"),
	
	url(r'^jobmap/',				"company_tree.immutable_views.jobmap", name="jobmap"),
	('^$',						"company_tree.immutable_views.jobmap"),
	
	##########################################################################################################################################
	
	(r'^airport/',					include("airport.urls")),
	(r'^aircraft/',					include("aircraft.urls")),
	(r'^mins/',					include("mins.urls")),
	(r'^company/',					include("company_tree.urls_company")),
	(r'^position/',					include("company_tree.urls_position")),
	(r'^fleet/',					include("company_tree.urls_fleet")),
	
	###########################################################################################################################################
	
	url(r'^operation/edit/(?P<pk>\d{1,4})/$',	"company_tree.views.edit_operation", name="edit-operation"),
	url(r'^operation/new/(?P<pk>\d{1,4})/$',	"company_tree.views.new_operation", name="new-operation"),
	
	#(r'^route/edit/(?P<pk>\d{1,4})/$',		"route.views.handle_route", {"type": "edit"}),
	#(r'^route/new/(?P<pk>\d{1,4})/$',		"route.views.handle_route", {"type": "new"}),

	
	
	###########################################################################################################################################
	
	#(r'^kml/position-(?P<position>\d{1,4}).kml$',	"company_tree.views_map.kml"),
	#(r'^kml/company-(?P<company>\d{1,4}).kml$',	"company_tree.views_map.kml"),
	#(r'^kml/airport-(?P<airport>[A-Z]{1,5}).kml$',	"company_tree.views_map.kml"),
	
	###########################################################################################################################################
)

urlpatterns += patterns('django.contrib.auth',
	(r'^accounts/logout/$','views.logout', {"template_name": "view_jobmap.html"}),
)
