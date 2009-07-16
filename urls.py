from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

	(r'^overlay/(?P<z>\d{1,2})_(?P<x>\d{1,5})_(?P<y>\d{1,5})_(?P<o>\S{1,5})/$', 'main.views.overlay'),
	(r'^map_click/(?P<z>\d{1,2})_(?P<lat>\-?\d+\.\d*)_(?P<lng>\-?\d+\.\d*)/$',		'main.views.map_click'),
	
	(r'^admin/doc/',						include('django.contrib.admindocs.urls')),
	(r'^comments/',							include('django.contrib.comments.urls')),
	(r'^admin/(.*)',						admin.site.root),
	(r'^openid/',							include('django_openid_auth.urls')),
	
	
	(r'^site-media/(?P<path>.*)$',					'django.views.static.serve', {'document_root': '/home/chris/Websites/jobmap/media', 'show_indexes': True}),
	
	(r'^profile/',							"main.views.profile"),
	
	url(r'^jobmap/',						"main.views_map.jobmap", name="jobmap"),
	url('^$',							"main.views_map.jobmap", name="root"),
	
	##########################################################################################################################################
	
	(r'^airport/',					include("airport.urls")),
	(r'^aircraft/',					include("aircraft.urls")),
	(r'^mins/',					include("main.urls_mins")),
	(r'^company/',					include("main.urls_company")),
	(r'^position/',					include("main.urls_position")),
	(r'^fleet/',					include("main.urls_fleet")),
	(r'^operation/',				include("main.urls_operation")),
	
	###########################################################################################################################################
	
	#(r'^kml/position-(?P<position>\d{1,4}).kml$',			"jobmap.main.views.kml"),
	#(r'^kml/company-(?P<company>\d{1,4}).kml$',			"jobmap.main.views.kml"),
	#(r'^kml/airport-(?P<airport>[A-Z]{1,5}).kml$',			"jobmap.main.views.kml"),
	
	###########################################################################################################################################
	
	#(r'^company/list/$',						"jobmap.main.list_views.company"),
	#(r'^position/list/$',						"jobmap.main.list_views.position"),
	#(r'^aircraft/list/$',						"jobmap.main.list_views.aircraft"),
	
)

urlpatterns += patterns('django.contrib.auth',
#	(r'^accounts/login/$','views.login', {'template_name': 'admin/login.html'}),
	(r'^accounts/logout/$','views.logout', {"template_name": "view_jobmap.html"}),
)
