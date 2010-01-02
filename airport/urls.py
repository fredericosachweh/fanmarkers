from django.conf.urls.defaults import *

urlpatterns = patterns('airport',

        url(
            r'^(?P<ident>\S{1,7}).html$',
            "views.airport",
                                                           name="view-airport",
        ),
        
        url(
            r'^(?P<ident>[A-Z0-9]{1,7}).kmz$',
            "views.kmz",
                                                            name="kml-airport",
        ),
)
