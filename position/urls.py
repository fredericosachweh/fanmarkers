from django.conf.urls.defaults import *

urlpatterns = patterns('position',
    url(r'^$',                      "views.make_list", name="list-position"),
    url(r'^(?P<pk>\d{1,4}).html$',  "views.view", name="view-position"),
    url(r'^new/(?P<pk>\d{1,4})/$',  "views.new", name="new-position"),
    url(r'^edit/(?P<pk>\d{1,4})/$', "views.edit", name="edit-position"),
)
