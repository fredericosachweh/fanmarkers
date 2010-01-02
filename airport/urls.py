from django.conf.urls.defaults import *

urlpatterns = patterns('airport',
        #url(r'^export$',              "views.export", name="export-airports"),
        url(r'^(?P<ident>\S{1,7}).html$',"views.airport", name="view-airport"),
)
