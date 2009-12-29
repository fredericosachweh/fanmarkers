from django.conf.urls.defaults import *

urlpatterns = patterns('fleet',
        url(r'^new/(?P<pk>\d+)/$',          "views.new", name="new-fleet"),
        url(r'^edit/(?P<pk>\d+)/$',         "views.edit", name="edit-fleet"),
)
