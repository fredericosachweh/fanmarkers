from django.conf.urls.defaults import *
from django.views.generic import list_detail, create_update
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

	(r'^overlay/(?P<z>\d{1,2})_(?P<x>\d{1,5})_(?P<y>\d{1,5})_(?P<o>\S{1,5})/$', 		'main.views_map.overlay'),
	(r'^map_click/(?P<z>\d{1,2})_(?P<lat>\-?\d+\.\d*)_(?P<lng>\-?\d+\.\d*)/$',		'main.views_map.click'),
	url(r'^jobmap/',									"main.views_map.jobmap", name="jobmap"),
	url('^$',										"main.views_map.jobmap", name="root"),
	
	(r'^admin/doc/',				include('django.contrib.admindocs.urls')),
	(r'^comments/',					include('django.contrib.comments.urls')),
	(r'^admin/(.*)',				admin.site.root),
	(r'^openid/',					include('django_openid_auth.urls')),
	
	
	(r'^site-media/(?P<path>.*)$',			'django.views.static.serve', {'document_root': '/home/chris/Websites/jobmap/media', 'show_indexes': True}),
	
	(r'^profile/',					"main.views.profile"),
	
	##########################################################################################################################################
	
	(r'^airport/',					include("airport.urls")),
	(r'^aircraft/',					include("aircraft.urls")),
	(r'^route/',					include("route.urls")),
	#url(r'dd', 'main.views_map.jobmap', name="edit-route"),
	#url(r'dd', 'main.views_map.jobmap', name="new-route"),
	
	(r'^mins/',					include("main.urls_mins")),
	(r'^company/',					include("main.urls_company")),
	(r'^position/',					include("main.urls_position")),
	(r'^fleet/',					include("main.urls_fleet")),
	(r'^operation/',				include("main.urls_operation")),
	
	
	###########################################################################################################################################
	
	(r'^kml/position-(?P<position>\d{1,4}).kml$',	"main.views_map.kml"),
	(r'^kml/company-(?P<company>\d{1,4}).kml$',	"main.views_map.kml"),
	(r'^kml/airport-(?P<airport>\S{1,7}).kml$',	"main.views_map.kml"),
	
)

urlpatterns += patterns('django.contrib.auth',
#	(r'^accounts/login/$','views.login', {'template_name': 'admin/login.html'}),
	(r'^accounts/logout/$','views.logout', {"template_name": "view_jobmap.html"}),
)
