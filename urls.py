from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to, direct_to_template
from django.contrib import admin
from sitemaps import *

#django_cron.autodiscover()
admin.autodiscover()

sitemaps = {"company": CompanySitemap,
            "aircraft": AircraftSitemap,
            "position": PositionSitemap,
            "airport": AirportSitemap,
           }


urlpatterns = patterns('',

    (r'^overlay/(?P<z>\d{1,2})_(?P<x>\d{1,5})_(?P<y>\d{1,5})_(?P<o>\S{1,5})/$',         'main.views_map.overlay'),
    (r'^map_click/(?P<z>\d{1,2})_(?P<lat>\-?\d+\.\d*)_(?P<lng>\-?\d+\.\d*)/$',          'main.views_map.click'),

    #################################################################################################################

    url('^$',                           redirect_to, {'url': 'about/'}),

    (r'^admin/',                        include(admin.site.urls)),
    (r'^admin/doc/',                    include('django.contrib.admindocs.urls')),
    (r'^comments/',                     include('mod_comments.urls')),
    
    (r'^sitemap.xml$',                  'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^robots.txt$',                   include('robots.urls')),
    
    (r'^site-media/(?P<path>.*)$',      'django.views.static.serve', {'document_root': '/home/chris/Websites/fanmarkers/media', 'show_indexes': True}),

    
    #################################################################################################################


    (r'^airport/',              include("airport.urls")),
    (r'^aircraft/',             include("aircraft.urls")),
    (r'^route/',                include("route.urls")),

    (r'^mins/',                 include("main.urls_mins")),
    (r'^company/',              include("main.urls_company")),
    (r'^position/',             include("main.urls_position")),
    (r'^fleet/',                include("main.urls_fleet")),
    (r'^operation/',            include("main.urls_operation")),

    url(r'^latest/$',           "main.views.latest", name="latest"),
    url(r'^about/$',            "main.views.about", name="about" ),
    url(r'^jobmap/',            "main.views_map.jobmap", name="jobmap"),
    url(r'^profile/',           "profile.views.profile", name="profile"),

    (r'^openid/',               include('django_openid_auth.urls')),

###########################################################################################################################################

    (r'^kml/position-(?P<position>\d+).kml$',   "main.views_map.kml"),
    (r'^kml/company-(?P<company>\d+).kml$',     "main.views_map.kml"),
    (r'^kml/airport-(?P<airport>\S+).kml$',     "main.views_map.kml"),

)

urlpatterns += patterns('django.contrib.auth',
    url(r'^accounts/logout/$','views.logout', {"template_name": "about.html"}, name="logout"),
)


