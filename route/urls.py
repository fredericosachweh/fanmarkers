from django.conf.urls.defaults import *

urlpatterns = patterns('route',
        url(r'^new/(?P<pk>\d{1,4})/$',          "views.handle_route", {"type": "new"}, name="new-route"),
        url(r'^edit/(?P<pk>\d{1,4})/$',         "views.handle_route", {"type": "edit"}, name="edit-route"),
)
