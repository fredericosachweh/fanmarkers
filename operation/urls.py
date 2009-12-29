from django.conf.urls.defaults import *

urlpatterns = patterns('operation',
    url(r'^new/(?P<pk>\d{1,4})/$', "views.new", name="new-operation"),
    url(r'^edit/(?P<pk>\d{1,4})/$', "views.edit", name="edit-operation"),
)
