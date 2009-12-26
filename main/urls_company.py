from django.conf.urls.defaults import *

urlpatterns = patterns('main',
        url(r'^$',                                               "views_company.make_list", name="list-company"),
        url(r'^(?P<pk>\d*)-(?P<slug>[a-z0-9\-]*).html$',         "views_company.view", name="view-company"),
        url(r'^new/$',                                           "views_company.new", name="new-company"),
        url(r'^edit/(?P<pk>\d{1,4})/$',                          "views_company.edit", name="edit-company"),
)
