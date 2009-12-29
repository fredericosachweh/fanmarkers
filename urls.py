from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to, direct_to_template

################################################

from django.contrib import admin

admin.autodiscover()

#################################################

from sitemaps import *

sitemaps = {"company": CompanySitemap,
            "aircraft": AircraftSitemap,
            "position": PositionSitemap,
            "airport": AirportSitemap,
           }

#################################################

urlpatterns = patterns('',

    (r'^overlay/(?P<z>\d{1,2})_(?P<x>\d{1,5})_(?P<y>\d{1,5})_(?P<o>\S{1,5})/$',
                                'jobmap.views.overlay'),
                            
    (r'^map_click/(?P<z>\d{1,2})_(?P<lat>\-?\d+\.\d*)_(?P<lng>\-?\d+\.\d*)/$',
                                'jobmap.views.click'),

    ###########################################################################

    url('^$',                   redirect_to, {'url': 'about.html'}),

    (r'^admin/',                include(admin.site.urls)),
    (r'^admin/doc/',            include('django.contrib.admindocs.urls')),
    (r'^comments/',             include('mod_comments.urls')),
    
    (r'^robots.txt$',           include('robots.urls')),
    
    ###########################################################################

    (r'^airport/',              include("airport.urls")),
    (r'^aircraft/',             include("aircraft.urls")),
    (r'^route/',                include("route.urls")),

    (r'^mins/',                 include("mins.urls")),
    (r'^company/',              include("company.urls")),
    (r'^position/',             include("position.urls")),
    #(r'^fleet/',                include("company.urls_fleet")),
    (r'^operation/',            include("operation.urls")),

    #url(r'^latest.html$',       "main.views.latest", name="latest"),
    #url(r'^about.html$',        "main.views.about", name="about" ),
    url(r'^jobmap.html',        "jobmap.views.jobmap", name="jobmap"),
    url(r'^profile.html',       "profile.views.profile", name="profile"),

    (r'^openid/',               include('django_openid_auth.urls')),

###############################################################################

    (r'^kml/position-(?P<position>\d+).kml$',   "jobmap.views.kml"),
    (r'^kml/company-(?P<company>\d+).kml$',     "jobmap.views.kml"),
    (r'^kml/airport-(?P<airport>\S+).kml$',     "jobmap.views.kml"),

    (
        r'^dev-media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': '/srv/fanmarkers/media', 'show_indexes': True}
    ),
    
    (
        r'^sitemap.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}
    ),

)

urlpatterns += patterns('django.contrib.auth',
    url(
        r'^accounts/logout/$','views.logout',
        {"template_name": "about.html"},                        name="logout"),
)


