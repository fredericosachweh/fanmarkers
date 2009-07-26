from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    (r'^overlay/(?P<z>\d{1,2})_(?P<x>\d{1,5})_(?P<y>\d{1,5})_(?P<o>\S{1,5})/$',         'main.views_map.overlay'),
    (r'^map_click/(?P<z>\d{1,2})_(?P<lat>\-?\d+\.\d*)_(?P<lng>\-?\d+\.\d*)/$',          'main.views_map.click'),

    url(r'^jobmap/',                            "main.views_map.jobmap", name="jobmap"),
    url('^$',                                   "main.views_map.jobmap", name="root"),

    (r'^admin/doc/',                            include('django.contrib.admindocs.urls')),
    (r'^comments/',                             include('mod_comments.urls')),

    (r'^admin/(.*)',                            admin.site.root),
    (r'^openid/',                               include('django_openid_auth.urls')),

    (r'^site-media/(?P<path>.*)$',              'django.views.static.serve', {'document_root': '/home/chris/Websites/jobmap/media', 'show_indexes': True}),

    (r'^profile/',                              "main.views.profile"),

    ##########################################################################################################################################

    (r'^airport/',              include("airport.urls")),
    (r'^aircraft/',             include("aircraft.urls")),
    (r'^route/',                include("route.urls")),

    (r'^mins/',                 include("main.urls_mins")),
    (r'^company/',              include("main.urls_company")),
    (r'^position/',             include("main.urls_position")),
    (r'^fleet/',                include("main.urls_fleet")),
    (r'^operation/',            include("main.urls_operation")),

    url(r'^latest/$',           "main.views.latest", name="latest"),
    url(r'^about/$',            direct_to_template, {'template': 'about.html'}, name="about" ),


###########################################################################################################################################

    (r'^kml/position-(?P<position>\d+).kml$',   "main.views_map.kml"),
    (r'^kml/company-(?P<company>\d+).kml$',     "main.views_map.kml"),
    (r'^kml/airport-(?P<airport>\S+).kml$',     "main.views_map.kml"),

)

urlpatterns += patterns('django.contrib.auth',
    url(r'^accounts/logout/$','views.logout', {"template_name": "view_jobmap.html"}, name="logout"),
)
