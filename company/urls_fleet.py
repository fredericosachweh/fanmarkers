from django.conf.urls.defaults import *

urlpatterns = patterns('main',
        url(r'^new/(?P<pk>\d+)/$',          "views_fleet.new", name="new-fleet"),
        url(r'^edit/(?P<pk>\d+)/$',         "views_fleet.edit", name="edit-fleet"),
)
